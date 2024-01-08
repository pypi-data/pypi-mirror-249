from abc import ABC, abstractmethod
import logging
from typing import Any, Dict, Optional
from pyspark.sql import SparkSession, DataFrame

logger = logging.getLogger(__name__)


class TransformerException(Exception):
    pass


class Transformer(ABC):
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__()
        logger.info(f"[__init__|in] ({config})")
        self._config = config
        logger.info(f"[__init__|out]")

    @property
    def sink():
        pass

    # @abstractmethod
    def process(self, obj: Any) -> Any:
        raise NotImplementedError()


class SparkProcessor(Processor):
    def __init__(self, config: Optional[Dict[str, Any]] = None, spark: Optional[SparkSession] = None):
        super().__init__(config=config)
        self._spark = spark

    @abstractmethod
    def process(self, obj: DataFrame) -> DataFrame:
        raise NotImplementedError()
