from time import sleep
import numpy as np
from SmartApi.smartExceptions import DataException
from volstreet import config
from volstreet.config import token_exchange_dict, logger
from volstreet.utils import custom_round
from volstreet.angel_interface.fetching import fetch_book, lookup_and_return, LiveFeeds
from volstreet.angel_interface.active_session import ActiveSession


def place_order(
    symbol: str,
    token: str,
    qty: int,
    action: str,
    price: str | float,
    order_tag: str = "",
    stop_loss_order: bool = False,
) -> str:
    """Price can be a str or a float because "market" is an acceptable value for price."""
    action = action.upper()
    if isinstance(price, str):
        price = price.upper()
    exchange = token_exchange_dict[token]
    params = {
        "tradingsymbol": symbol,
        "symboltoken": token,
        "transactiontype": action,
        "exchange": exchange,
        "producttype": "CARRYFORWARD",
        "duration": "DAY",
        "quantity": int(qty),
        "ordertag": order_tag,
    }

    if stop_loss_order:
        execution_price = price * 1.1
        params.update(
            {
                "variety": "STOPLOSS",
                "ordertype": "STOPLOSS_LIMIT",
                "triggerprice": round(price, 1),
                "price": round(execution_price, 1),
            }
        )
    else:
        order_type, execution_price = (
            ("MARKET", 0) if price == "MARKET" else ("LIMIT", price)
        )
        execution_price = custom_round(execution_price)
        params.update(
            {"variety": "NORMAL", "ordertype": order_type, "price": execution_price}
        )

    for attempt in range(1, 4):
        try:
            return ActiveSession.obj.placeOrder(params)
        except Exception as e:
            if attempt == 3:
                raise e
            logger.error(
                f"Error {attempt} in placing {'stop-loss ' if stop_loss_order else ''}order for {symbol}: {e}"
            )
            sleep(1)


def handle_open_orders_turbo(order_ids, current_iteration=0):
    """Modifies orders if they are pending by the provided modification percentage"""
    modify_percentage = config.MODIFICATION_STEP_SIZE
    max_modification = config.MAX_PRICE_MODIFICATION
    max_iterations = max(int(max_modification / modify_percentage), 1)

    if current_iteration >= max_iterations:
        logger.info("Max iterations reached, exiting modification")
        return

    order_book = LiveFeeds.order_book

    # Extracting only the open orders from the order book
    open_order_params: np.ndarray[dict] = lookup_and_return(
        order_book,
        ["orderid", "status"],
        [order_ids, ["open", "open pending", "modified", "modify pending"]],
        config.modification_fields,
    )
    if len(open_order_params) == 0:
        logger.debug("No open orders found, exiting modification")
        return

    _modify(open_order_params, modify_percentage)

    open_order_ids = [order["orderid"] for order in open_order_params]
    return handle_open_orders_turbo(open_order_ids, current_iteration + 1)


def _modify(
    open_orders_params: list[dict] | np.ndarray[dict], modify_percentage: float
):
    for order in open_orders_params:
        old_price = order["price"]
        action = order["transactiontype"]

        increment = max(0.2, old_price * modify_percentage)
        new_price = old_price + increment if action == "BUY" else old_price - increment
        new_price = max(0.05, new_price)
        new_price = custom_round(new_price)

        modified_params = order.copy()
        modified_params["price"] = new_price
        order["price"] = new_price
        modified_params.pop("status")

        try:
            ActiveSession.obj.modifyOrder(modified_params)
        except Exception as e:
            if isinstance(e, DataException):
                sleep(1)
            logger.error(f"Error in modifying order: {e}")


def handle_open_orders_back_up(
    order_ids: list[str] | tuple[str] | np.ndarray[str],
    orderbook: str | list = "orderbook",
):
    """Modifies orders if they are pending by the provided modification percentage"""

    modify_percentage = config.MODIFICATION_STEP_SIZE
    max_modification = config.MAX_PRICE_MODIFICATION
    iterations = max(int(max_modification / modify_percentage), 1)

    orderbook = fetch_book(orderbook) if isinstance(orderbook, str) else orderbook
    open_order_params: np.ndarray[dict] = lookup_and_return(
        orderbook,
        ["orderid", "status"],
        [order_ids, ["open", "open pending", "modified", "modified pending"]],
        config.modification_fields,
    )

    if len(open_order_params) == 0:
        logger.debug("No open orders found, exiting modification")
        return
    for i in range(iterations):
        _modify(open_order_params, modify_percentage)


def handle_open_orders(
    order_ids: list[str] | tuple[str] | np.ndarray[str],
    orderbook: str | list = "orderbook",
):
    if LiveFeeds.order_feed_connected():
        logger.info(f"Using turbo mode to modify orders")
        return handle_open_orders_turbo(order_ids)
    else:
        logger.debug(f"Using backup mode to modify orders")
        return handle_open_orders_back_up(order_ids, orderbook)
