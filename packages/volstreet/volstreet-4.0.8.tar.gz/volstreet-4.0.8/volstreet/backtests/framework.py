from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from datetime import datetime
from enum import Enum
from sqlalchemy import text
from volstreet.config import logger
from volstreet.utils.core import find_strike
from volstreet.backtests.underlying_info import UnderlyingInfo
from volstreet.backtests.backtester import BackTester


class Signal(Enum):
    BUY = 1
    SELL = -1


class IntradayBackTest(BackTester, ABC):
    def __init__(self, underlying: UnderlyingInfo):
        self.underlying = underlying
        self.expiry = None
        self._option_prices = pd.DataFrame()
        self.unique_strikes = []
        super().__init__()

    @property
    def option_prices(self):
        return self._option_prices

    @option_prices.setter
    def option_prices(self, new_prices):
        assert isinstance(new_prices, pd.DataFrame)
        if self.expiry is not None:
            assert new_prices.expiry.unique() == self.expiry.strftime("%d%b%y").upper()
        self._option_prices = (
            new_prices.reset_index()
            .drop_duplicates(subset=["timestamp", "strike", "expiry"])
            .set_index("timestamp")
        )
        self.unique_strikes = np.unique(
            self.unique_strikes + new_prices.strike.unique().tolist()
        ).tolist()

    def determine_expiry(self, initiation_info: pd.Series):
        nearest_expiry = self.fetch_nearest_expiry_from_date(
            self.underlying.name, initiation_info.name
        )
        return nearest_expiry

    def snapshot_at_entry(
        self, initiation_info: pd.Series, num_strikes: int
    ) -> pd.DataFrame:
        """Currently only supports straddle and not strangle"""
        initiation_info = initiation_info.to_frame().T
        snapshot = self._build_option_chain_skeleton(
            self.underlying.name, initiation_info, num_strikes, threshold_days_expiry=0
        )
        return snapshot

    def fetch_and_store_option_prices(
        self,
        initiation_info: pd.Series,
        num_strikes: int,
    ):
        """This function will take in the daily prices of the index"""

        atm_strike = find_strike(initiation_info.open, self.underlying.base)
        strike_range = np.arange(
            atm_strike - num_strikes * self.underlying.base,
            atm_strike + num_strikes * self.underlying.base + self.underlying.base,
            self.underlying.base,
        )
        query = self.generate_query_for_option_prices(
            self.underlying.name,
            [self.expiry.strftime("%d%b%y").upper()],
            [strike for strike in strike_range],
            from_date=initiation_info.name.strftime("%Y-%m-%d %H:%M"),
            to_date=self.expiry.strftime("%Y-%m-%d %H:%M"),
        )
        prices = self.fetch_option_prices(query)
        prices = self.rearrange_options_prices(prices).rename(
            columns={"CE": "call_price", "PE": "put_price"}
        )
        self.option_prices = pd.concat([self.option_prices, prices]).sort_index()

        return prices

    def fetch_missed_strikes(
        self,
        strikes: list[int | float],
        from_date: datetime,
    ):
        query = self.generate_query_for_option_prices(
            self.underlying.name,
            [self.expiry.strftime("%d%b%y").upper()],
            strikes,
            from_date=from_date.strftime("%Y-%m-%d %H:%M"),
            to_date=self.expiry.strftime("%Y-%m-%d %H:%M"),
        )
        prices = self.fetch_option_prices(query)
        prices = self.rearrange_options_prices(prices).rename(
            columns={"CE": "call_price", "PE": "put_price"}
        )
        self.option_prices = pd.concat([self.option_prices, prices]).sort_index()

    def strike_available(self, new_strikes: list[int | float]) -> list[bool]:
        return [strike in self.unique_strikes for strike in new_strikes]

    def check_option_prices_availability(
        self,
        date_frame_to_merge: pd.DataFrame,
    ) -> None:
        option_prices = self.option_prices.reset_index()
        date_frame_to_merge = date_frame_to_merge.reset_index()

        # Get the list of strike columns from the subclass
        strike_columns = self.get_strike_columns()

        # Create a set of unique combinations of timestamp and strikes from the option_prices DataFrame
        available_options = set(
            option_prices[["timestamp", "strike"]].apply(tuple, axis=1)
        )

        # Initialize a DataFrame to hold all missing strike information
        missing_strikes_info = pd.DataFrame()

        # Check for strike availability for each specified column
        for strike_col in strike_columns:
            missing_strikes = date_frame_to_merge[
                ~date_frame_to_merge[["timestamp", strike_col]]
                .apply(tuple, axis=1)
                .isin(available_options)
            ]

            # Add a column to specify the type of strike that is missing
            missing_strikes["missing_strike_type"] = strike_col

            # Append missing strikes to the info DataFrame
            missing_strikes_info = pd.concat(
                [missing_strikes_info, missing_strikes], ignore_index=True
            )

        # Report missing strikes
        if not missing_strikes_info.empty:
            logger.error(
                f"Missing option price data for the following combinations:\n{missing_strikes_info}"
            )

    @abstractmethod
    def get_strike_columns(self):
        pass


def generate_cte_entries(
    dataframe: pd.DataFrame,
    timestamp_col: str,
    strike_col: str,
    expiry_col: str,
    option_type: str,
):
    cte_entries = [
        f"('{row[timestamp_col]}'::timestamp, {row[strike_col]}::integer, '{row[expiry_col]}'::text, '{option_type}'::text)"
        for _, row in dataframe.iterrows()
    ]
    return cte_entries


def generate_cte_entries_from_df(dataframe: pd.DataFrame) -> list:
    cte_entries = []

    for col in dataframe.columns:
        if "strike" in col:
            # Determine option type
            option_type = "CE" if "call" in col else "PE"

            # Determine the correct timestamp and expiry columns
            if "square_up" in col:
                timestamp_col = "square_up_timestamp"
                expiry_col = "square_up_expiry"
            else:
                timestamp_col = "timestamp"
                expiry_col = "expiry"

            # Generate CTE entries
            entries = generate_cte_entries(
                dataframe, timestamp_col, col, expiry_col, option_type
            )
            cte_entries.extend(entries)

    return cte_entries


def convert_cte_entries_to_query(
    cte_entries: list,
    underlying: str,
    cols_to_return: list | None = None,
) -> text:
    if cols_to_return is None:
        cols_to_return = ["timestamp", "expiry", "strike", "option_type", "close"]

    # Join the entries with a comma to create a single string
    cte_entries_str = ", ".join(cte_entries)
    columns_str = ", ".join([f"index_options.{x}" for x in cols_to_return])

    cte = f"WITH conditions AS (SELECT * FROM (VALUES {cte_entries_str}) AS t(timestamp, strike, expiry, option_type))"

    sql_query = text(
        f"""
        {cte}
        SELECT {columns_str}
        FROM index_options
        INNER JOIN conditions
        ON index_options.timestamp = conditions.timestamp 
           AND index_options.expiry = conditions.expiry
           AND index_options.strike = conditions.strike
           AND index_options.option_type = conditions.option_type
        WHERE index_options.underlying = '{underlying}';
        """
    )

    return sql_query


def melt_frame(
    trade_df: pd.DataFrame,
    leg_type: str,
    square_up: bool,
) -> pd.DataFrame:
    timestamp_col = "square_up_timestamp" if square_up else "timestamp"
    expiry_col = "square_up_expiry" if square_up else "expiry"
    leg_cols = [
        col for col in trade_df.columns if f"{leg_type}" in col and "strike" in col
    ]
    melted_df = pd.melt(
        trade_df,
        ["trade_id", timestamp_col, expiry_col],
        leg_cols,
        f"{leg_type}_leg",
        f"strike",
    )

    melted_df[f"{leg_type}_leg"] = melted_df[f"{leg_type}_leg"].str.replace(
        "_strike", ""
    )

    return melted_df


def merge_with_option_prices(
    melted_df: pd.DataFrame,
    option_prices_df: pd.DataFrame,
    leg_type: str,
    square_up: bool,
) -> pd.DataFrame:
    """
    Merge the melted legs data with the option prices dataframe.
    """
    price_column = f"{leg_type}_price"
    timestamp_col = "square_up_timestamp" if square_up else "timestamp"
    expiry_col = "square_up_expiry" if square_up else "expiry"
    if square_up:
        option_prices_df = option_prices_df.rename(
            columns={
                "timestamp": "square_up_timestamp",
                "expiry": "square_up_expiry",
            }
        )

    return pd.merge(
        melted_df,
        option_prices_df[[timestamp_col, expiry_col, f"strike", price_column]],
        left_on=[timestamp_col, expiry_col, f"strike"],
        right_on=[timestamp_col, expiry_col, f"strike"],
        how="left",
    )


def pivot_frame(
    merged_df: pd.DataFrame,
    leg_type: str,
    square_up: bool,
) -> pd.DataFrame:
    timestamp_col = "square_up_timestamp" if square_up else "timestamp"
    expiry_col = "square_up_expiry" if square_up else "expiry"

    pivoted = merged_df.pivot_table(
        index=["trade_id", timestamp_col, expiry_col],
        columns=f"{leg_type}_leg",
        values=[f"strike", f"{leg_type}_price"],
        aggfunc="first",
    )

    pivoted = pivoted.rename(columns={f"{leg_type}_price": "price"})

    pivoted.columns = [
        f"{col[1]}_{col[0]}" if col[0] in ["strike", "price"] else col[1]
        for col in pivoted.columns.values
    ]
    return pivoted.reset_index()


def add_option_prices_to_leg(trade_df, option_prices_df, leg_type, square_up=False):
    """
    A generalized function to process either trade or square-up legs.
    """
    if square_up:
        trade_df = trade_df.filter(regex="^square_up_|^trade_id$")
    else:
        # Filter out square-up columns
        trade_df = trade_df.filter(regex="^(?!square_up_)")

    legs_df = melt_frame(trade_df, leg_type, square_up)

    merged_df = merge_with_option_prices(legs_df, option_prices_df, leg_type, square_up)

    return pivot_frame(merged_df, leg_type, square_up)


def populate_with_option_prices(trade_df, option_prices_df, has_square_up=False):
    """
    Refactored function to process trade data and merge with option prices. The trade_df should
    contain the following columns:
    - trade_id
    - timestamp
    - expiry
    and call and put strike columns.
    """
    call_trades = add_option_prices_to_leg(trade_df, option_prices_df, "call")
    put_trades = add_option_prices_to_leg(trade_df, option_prices_df, "put")
    merged_trades = call_trades.merge(
        put_trades, on=["trade_id", "timestamp", "expiry"], how="left"
    )
    if not has_square_up:
        return merged_trades

    square_up_call_trades = add_option_prices_to_leg(
        trade_df, option_prices_df, "call", True
    )
    square_up_put_trades = add_option_prices_to_leg(
        trade_df, option_prices_df, "put", True
    )
    square_up_trades = square_up_call_trades.merge(
        square_up_put_trades,
        on=["trade_id", "square_up_timestamp", "square_up_expiry"],
        how="left",
    )
    merged_with_square_up = merged_trades.merge(
        square_up_trades,
        on=["trade_id"],
        how="left",
    )
    return merged_with_square_up


def generate_sample_skeleton(with_square_up=False, hedge_leg=None):
    """For testing purposes only"""
    # Sample data for Skeleton DataFrame
    # Timestamps
    timestamps = pd.date_range(start="2023-01-01", periods=10, freq="D")

    # Expiry dates, let's assume they are weekly
    expiries = pd.date_range(start="2023-01-10", periods=2, freq="W")

    # Strike prices
    call_strikes = np.linspace(100, 110, 3)
    put_strikes = np.linspace(100, 110, 3)

    # Creating a grid of all combinations
    skeleton_data = pd.MultiIndex.from_product(
        [timestamps, expiries, zip(call_strikes, put_strikes)],
        names=["timestamp", "expiry", "strikes"],
    ).to_frame(index=False)
    skeleton_data.drop_duplicates(subset=["timestamp"], inplace=True, keep="first")
    skeleton_data["call_strike"] = skeleton_data["strikes"].apply(lambda x: x[0])
    skeleton_data["put_strike"] = skeleton_data["strikes"].apply(lambda x: x[1])
    skeleton_data.drop(columns=["strikes"], inplace=True)

    if hedge_leg:
        skeleton_data[f"{hedge_leg}_hedge_strike"] = (
            skeleton_data[f"{hedge_leg}_strike"] + 5
            if hedge_leg == "call"
            else skeleton_data[f"{hedge_leg}_strike"] - 5
        )

    if with_square_up:
        # Adding square up columns to the skeleton data
        skeleton_data["square_up_timestamp"] = skeleton_data["timestamp"]
        skeleton_data["square_up_expiry"] = skeleton_data["expiry"].shift(1)
        skeleton_data["square_up_call_strike"] = skeleton_data["call_strike"].shift(1)
        skeleton_data["square_up_put_strike"] = skeleton_data["put_strike"].shift(1)
        if hedge_leg:
            skeleton_data[f"square_up_{hedge_leg}_hedge_strike"] = skeleton_data[
                f"{hedge_leg}_hedge_strike"
            ].shift(1)
    skeleton_data["trade_id"] = range(1, len(skeleton_data) + 1)
    return skeleton_data


def generate_sample_option_prices():
    """For testing purposes only"""
    timestamps = pd.date_range(start="2023-01-01", periods=10, freq="D")

    expiries = pd.date_range(start="2023-01-10", periods=2, freq="W")

    option_df_strikes = np.arange(90, 150, 5)
    option_prices_data = pd.MultiIndex.from_product(
        [timestamps, expiries, option_df_strikes],
        names=["timestamp", "expiry", "strike"],
    ).to_frame(index=False)
    option_prices_data["call_price"] = np.random.uniform(5, 15, len(option_prices_data))
    option_prices_data["put_price"] = np.random.uniform(3, 10, len(option_prices_data))

    return option_prices_data
