from ..utils import _Parseable
from ._base import Node

__all__ = ["Comment"]

class Comment(Node):
    def __init__(self, contents: _Parseable) -> None: ...
    def __strip__(
        self,
        *,
        normalize: bool = ...,
        collapse: bool = ...,
        keep_template_params: bool = ...,
    ) -> None: ...
    @property
    def contents(self) -> str: ...
    @contents.setter
    def contents(self, value: _Parseable) -> None: ...
