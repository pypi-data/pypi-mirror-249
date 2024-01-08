from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class SourceException(Exception):
    pass


class Source(ABC):
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__()
        self._config = config

    @abstractmethod
    def get(self, key: Any, **kwargs) -> Any:
        raise NotImplementedError()
