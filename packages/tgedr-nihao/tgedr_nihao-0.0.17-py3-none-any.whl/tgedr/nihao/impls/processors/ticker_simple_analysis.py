import logging
from typing import Any, Dict, Optional


from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F

from tgedr.nihao.commons.processor import SparkProcessor


logger = logging.getLogger(__name__)


class TickerSimpleAnalysis(SparkProcessor):
    def __init__(self, config: Optional[Dict[str, Any]] = None, spark: Optional[SparkSession] = None):
        super().__init__(config=config, spark=spark)

    def process(self, obj: DataFrame) -> DataFrame:
        logger.info(f"[process|in] ({obj})")
        result = (
            obj.filter(F.col("variable").isin(["Adj Close", "Volume"]))
            .groupBy(["symbol", "actual_time"])
            .pivot("variable")
            .max("value")
            .withColumnRenamed("Adj Close", "adj_close")
            .withColumnRenamed("Volume", "volume")
            .sort("actual_time", ascending=True)
        )
        logger.info(f"[process|out] => {result}")
        return result
