from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class SinkException(Exception):
    pass


class Sink(ABC):
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__()
        self._config = config

    @abstractmethod
    def put(self, obj: Any, key: Any, **kwargs) -> Any:
        raise NotImplementedError()
