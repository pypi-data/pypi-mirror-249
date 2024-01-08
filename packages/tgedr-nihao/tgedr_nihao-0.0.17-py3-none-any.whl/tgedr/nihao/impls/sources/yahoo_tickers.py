import logging
from typing import Any, Dict, List, Optional
import pandas as pd
import logging
import yfinance as yf

from tgedr.nihao.commons.source import Source


logger = logging.getLogger(__name__)


class YahooTickersSource(Source):
    __DEFAULT_INTERVAL: str = "1d"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)

    def get(self, key: str, **kwargs) -> pd.DataFrame:
        logger.info(f"[get|in] ({key}, {kwargs})")

        symbols_as_str = key
        symbols: List[str] = [k.strip() for k in symbols_as_str.split(",")]

        interval = self.__DEFAULT_INTERVAL
        if "interval" in kwargs:
            interval = kwargs["interval"]

        start = None
        if "start" in kwargs:
            start = kwargs["start"]

        end = None
        if "end" in kwargs:
            end = kwargs["end"]

        market_data = yf.download(symbols_as_str, start=start, end=end, interval=interval)
        result = self.__market_data_2_df_another_approach(market_data, symbols)
        result.reset_index(drop=True, inplace=True)
        result = result.sort_values(by=["actual_time", "symbol"])

        logger.info(f"[get|out] => {result}")
        return result

    def __market_data_2_df_another_approach(self, market_data, symbols: List[str]) -> pd.DataFrame:
        logger.info(f"[__market_data_2_df_another_approach|in] ({market_data}, {symbols})")
        result = pd.DataFrame(columns=["symbol", "variable", "value", "actual_time"])
        df_as_dict = {"symbol": [], "variable": [], "value": [], "actual_time": []}
        if not market_data.empty:
            multiple_symbols: bool = 1 < len(symbols)
            for key, val in market_data.to_dict().items():
                if multiple_symbols:
                    variable, symbol = key
                else:
                    variable = key
                    symbol = symbols[0]

                for ts, num in val.items():
                    if not pd.isnull(num):
                        (df_as_dict["symbol"]).append(symbol)
                        (df_as_dict["variable"]).append(variable)
                        (df_as_dict["value"]).append(num)
                        (df_as_dict["actual_time"]).append(ts.timestamp())

            result = pd.DataFrame.from_dict(df_as_dict)

        logger.info(f"[__market_data_2_df_another_approach|out] => {result}")
        return result
