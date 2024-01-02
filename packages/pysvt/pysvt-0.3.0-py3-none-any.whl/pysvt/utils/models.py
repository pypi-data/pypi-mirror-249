from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class _FuncModel:
    inputs: list[Any]
    output: Any
    name: str
    metadata: str


@dataclass()
class _ClsModel:
    init: list[Any]
    data: list[_FuncModel]


@dataclass(frozen=True)
class Result:
    data: Any
    valid: bool
