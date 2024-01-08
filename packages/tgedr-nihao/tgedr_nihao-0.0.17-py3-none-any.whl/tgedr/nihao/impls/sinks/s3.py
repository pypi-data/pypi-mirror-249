import logging
from typing import Any, Dict, Optional
import pandas as pd
import awswrangler as wr
import boto3

from tgedr.nihao.commons.sink import Sink, SinkException


logger = logging.getLogger(__name__)


class AwsPdDfParquetSink(Sink):
    __ALLOWED_MODES = ["append", "overwrite", "overwrite_partitions"]
    __DEFAULT_MODE = "overwrite"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        logger.info(f"[__init__|in] ({config})")
        super().__init__(config)
        if config is not None:
            if "region" in config:
                boto3.setup_default_session(region_name=config["region"])

        logger.info("[__init__|out]")

    def put(self, obj: pd.DataFrame, key: str, **kwargs) -> None:
        logger.info(f"[put|in] ({obj}, {key}, {kwargs})")
        partition_cols = None
        if "partition_cols" in kwargs:
            partition_cols = kwargs["partition_cols"]

        mode = self.__DEFAULT_MODE
        if "mode" in kwargs:
            mode = kwargs["mode"]
            if mode not in self.__ALLOWED_MODES:
                raise SinkException(f"[put] unknown mode ({mode}), please provide one of modes: {self.__ALLOWED_MODES}")

        write_output = wr.s3.to_parquet(df=obj, path=key, dataset=True, partition_cols=partition_cols, mode=mode)
        logger.info(f"[put] write output: {write_output}")
        logger.info(f"[put|out]")
