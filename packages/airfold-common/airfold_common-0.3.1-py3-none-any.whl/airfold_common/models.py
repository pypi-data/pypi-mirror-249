from enum import Enum
from typing import Any

from pydantic.main import BaseModel


class Spec(BaseModel):
    name: str
    spec: Any


class AISpec(BaseModel):
    system: str
    host: str


class CommandType(str, Enum):
    CREATE = "CREATE"
    DELETE = "DELETE"
    REPLACE = "REPLACE"
    RENAME = "RENAME"
    UNDELETE = "UNDELETE"
    FAIL = "FAIL"
    UPDATE = "UPDATE"

    def __str__(self):
        return self._name_
