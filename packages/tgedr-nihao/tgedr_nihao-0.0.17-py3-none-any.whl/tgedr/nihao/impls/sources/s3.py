import logging
from typing import Any, Dict, Optional
import pandas as pd
import awswrangler as wr
import boto3

from tgedr.nihao.commons.source import Source

logger = logging.getLogger(__name__)


class AwsParquetPdDfSource(Source):
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        logger.info(f"[__init__|in] ({config})")
        super().__init__(config)
        if config is not None:
            if "region" in config:
                boto3.setup_default_session(region_name=config["region"])

        logger.info("[__init__|out]")

    def get(self, key: str, **kwargs) -> pd.DataFrame:
        logger.info(f"[get|in] ({key})")
        result: pd.DataFrame = wr.s3.read_parquet(key, dataset=True)
        logger.info(f"[get|out] => {result}")
        return result
