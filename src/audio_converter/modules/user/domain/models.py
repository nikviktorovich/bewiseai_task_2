import dataclasses
from typing import Any


@dataclasses.dataclass
class User:
    id: Any
    access_token: str
