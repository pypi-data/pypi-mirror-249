import itertools
from collections import defaultdict
from time import sleep
from datetime import timedelta
from volstreet.config import logger, token_symbol_dict
from volstreet.utils import current_time, get_symbol_token, strike_range_different
from volstreet.angel_interface.active_session import ActiveSession
from volstreet.angel_interface.price_websocket import PriceWebsocket


class PriceFeed(PriceWebsocket):
    # noinspection PyMissingConstructor
    def __init__(
        self, webhook_url=None, correlation_id="default", default_strike_range=7
    ):
        auth_token = ActiveSession.login_data["data"]["jwtToken"]
        feed_token = ActiveSession.obj.getfeedToken()
        api_key = ActiveSession.obj.api_key
        client_code = ActiveSession.obj.userId
        super().__init__(auth_token, api_key, client_code, feed_token, correlation_id)
        self.webhook_url = webhook_url
        self.default_strike_range = default_strike_range
        self.underlying_options_subscribed = {}
        self.connection_stale = False
        self.subscribed_to_options = False

    def parse_price_dict(self):
        new_price_dict = {
            token_symbol_dict[token]: value for token, value in self.data_bank.items()
        }
        return new_price_dict

    def get_active_subscriptions(self, options_only=True) -> dict[int, list[str]]:
        active_subscriptions = defaultdict(list)
        for mode, exchange_subscriptions in self.input_request_dict.items():
            for exchange, tokens in exchange_subscriptions.items():
                if options_only and exchange in [1, 3]:
                    continue
                active_subscriptions[mode].extend(tokens)
        return dict(active_subscriptions)

    def get_active_strike_range(
        self, underlying, range_of_strikes: int = None
    ) -> list[int]:
        range_of_strikes = (
            self.default_strike_range if range_of_strikes is None else range_of_strikes
        )
        return underlying.get_active_strikes(range_of_strikes)

    @staticmethod
    def _get_tokens_for_strike_expiry(name: str, strike: int, expiry: str):
        try:
            _, call_token = get_symbol_token(name, expiry, strike, "CE")
        except Exception as e:
            logger.error(
                f"Error in fetching call token for {strike, expiry} for {name}: {e}"
            )
            call_token = "abc"
        try:
            _, put_token = get_symbol_token(name, expiry, strike, "PE")
        except Exception as e:
            logger.error(
                f"Error in fetching put token for {strike, expiry} for {name}: {e}"
            )
            put_token = "abc"
        return call_token, put_token

    def _prepare_subscription_dict(
        self,
        underlying,
        strike_range: list[int],
    ) -> dict[int, list[str]]:
        subscription_dict = defaultdict(list)
        expiry_sub_modes = {
            underlying.current_expiry: 3,
            underlying.next_expiry: 1,
            underlying.far_expiry: 1,
        }
        for expiry, mode in expiry_sub_modes.items():
            for strike in strike_range:
                call_token, put_token = self._get_tokens_for_strike_expiry(
                    underlying.name, strike, expiry
                )
                subscription_dict[mode].append(call_token)
                subscription_dict[mode].append(put_token)
        return dict(subscription_dict)

    def subscribe_indices(self, mode: int = 1):
        self.subscribe(
            ["99926000", "99926009", "99926037", "99926074", "99919000"], mode
        )

    def subscribe_options(self, *underlyings, range_of_strikes: int = None):
        for underlying in underlyings:
            strike_range = self.get_active_strike_range(underlying, range_of_strikes)
            subscription_dict = self._prepare_subscription_dict(
                underlying, strike_range=strike_range
            )
            for mode, tokens in subscription_dict.items():
                self.subscribe(tokens, mode)
            self.underlying_options_subscribed[underlying] = strike_range
        self.subscribed_to_options = True

    def update_strike_range(self):
        for underlying in self.underlying_options_subscribed:
            refreshed_strike_range = self.get_active_strike_range(underlying)
            current_strike_range = self.underlying_options_subscribed[underlying]

            if not strike_range_different(refreshed_strike_range, current_strike_range):
                continue

            new_strikes = set(refreshed_strike_range) - set(current_strike_range)
            obsolete_strikes = set(current_strike_range) - set(refreshed_strike_range)
            if len(new_strikes) >= 0.4 * len(current_strike_range):  # Hardcoded 40%
                logger.info(
                    f"New strike range for {underlying.name}: {refreshed_strike_range}. "
                    f"Old strike range: {current_strike_range}."
                )

                subscription_dict = self._prepare_subscription_dict(
                    underlying, strike_range=list(new_strikes)
                )
                unsubscription_dict = self._prepare_subscription_dict(
                    underlying, strike_range=list(obsolete_strikes)
                )
                for mode in subscription_dict:
                    self.subscribe(subscription_dict[mode], mode)
                for mode in unsubscription_dict:
                    self.unsubscribe(unsubscription_dict[mode], mode)

                # Updating the strike range in the underlying_options_subscribed dict
                self.underlying_options_subscribed[underlying] = refreshed_strike_range

                all_tokens_subscribed = list(
                    itertools.chain(*subscription_dict.values())
                )
                all_tokens_unsubscribed = list(
                    itertools.chain(*unsubscription_dict.values())
                )
                all_symbols_subscribed = [
                    token_symbol_dict[token] for token in all_tokens_subscribed
                ]
                all_symbols_unsubscribed = [
                    token_symbol_dict[token] for token in all_tokens_unsubscribed
                ]
                logger.debug(
                    f"{underlying.name} subscribed to: {all_symbols_subscribed} "
                    f"and unsubscribed from: {all_symbols_unsubscribed}"
                )

    def check_freshness_of_data(self):
        if self.data_bank:
            try:
                time_now = current_time()
                most_recent_timestamp = max(
                    [value["timestamp"] for value in self.data_bank.values()]
                )
                if time_now - most_recent_timestamp > timedelta(seconds=5):
                    self.connection_stale = True
                else:
                    self.connection_stale = False
            except Exception as e:
                logger.error(f"Error in checking freshness of data: {e}")

    def periodically_update_strike_range(self):
        while True and not self.intentionally_closed:
            if self.subscribed_to_options and not self.reconnecting:
                self.update_strike_range()
            sleep(5)

    def periodically_check_freshness_of_data(self):
        last_check_time = current_time()
        while True and not self.intentionally_closed:
            self.check_freshness_of_data()
            if current_time() - last_check_time > timedelta(seconds=30):
                logger.info(f"Connection stale status: {self.connection_stale}")
                last_check_time = current_time()
            sleep(5)
