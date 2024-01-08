from datetime import datetime
import logging
from typing import Optional
import pandas as pd
from tgedr.nihao.sink.s3 import PdDataFrameS3Sink
from tgedr.nihao.source.yahoo_tickers import YahooTickersSource


logger = logging.getLogger(__name__)


class Tickers2S3parquet:
    def fetch(
        self,
        tickers: str,
        target: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        interval: str = "1d",
    ):
        logger.info(f"[fetch|in] ({tickers}, {target}, {start}, {end}, {interval})")
        source = YahooTickersSource()
        df: pd.DataFrame = source.get(key=tickers, start=start, end=end, interval=interval)

        sink = PdDataFrameS3Sink(config={})
        sink.put(obj=df, key=target)
        logger.info("[fetch|out]")
