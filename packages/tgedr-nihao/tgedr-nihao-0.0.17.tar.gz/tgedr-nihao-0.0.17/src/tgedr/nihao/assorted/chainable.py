import logging
from typing import Any, Dict, Optional, Union
from tgedr.nihao.commons.processor import Processor
from tgedr.nihao.commons.sink import Sink
from tgedr.nihao.commons.source import Source


logger = logging.getLogger(__name__)


class ChainableException(Exception):
    pass


class ContextHandler:
    def __init__(self, read_handler: Optional[callable] = None, write_handler: Optional[callable] = None):
        self._reader: callable = read_handler
        self._writer: callable = write_handler

    def read(self, context: Dict[str, Any]) -> Any:
        if self._reader is not None:
            return self._reader(context)
        else:
            return None

    def write(self, context: Dict[str, Any], state: Any) -> None:
        if self._writer is not None:
            self._writer(context, state)
        else:
            return None


class Chainable:
    def __init__(self, whatever: Union[Source, Processor, Sink], context_handler: ContextHandler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._this: Union[Source, Processor, Sink] = whatever
        self._context_handler = context_handler
        self._next: "Chainable" = None

    def next(self, handler: "Chainable") -> "Chainable":
        if self._next is None:
            self._next: "Chainable" = handler
        else:
            self._next.next(handler)
        return self

    def _exec(self, context: Optional[Dict[str, Any]] = None, **kwargs) -> None:
        input = self._context_handler.read(context)

        if issubclass(self._this.__class__, Source):
            output: Any = self._this.get(key=input, **kwargs)
        elif issubclass(self._this.__class__, Processor):
            output: Any = self._this.process(obj=input, **kwargs)
        elif issubclass(self._this.__class__, Sink):
            input_0 = None
            input_1 = None
            if input is not None:
                input_0 = input[0]
                input_1 = input[1]

            output: Any = self._this.put(obj=input_0, key=input_1, **kwargs)
        else:
            raise ChainableException("chainables must be one of types: [Source, Processor, Sink]")

        self._context_handler._writer(context, output)

    def execute(self, context: Optional[Dict[str, Any]] = None) -> None:
        self._exec(context=context)
        if self._next is not None:
            self._next.execute(context=context)
