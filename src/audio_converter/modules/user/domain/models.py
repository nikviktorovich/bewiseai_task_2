import dataclasses
from typing import Any


@dataclasses.dataclass
class User:
    id: Any
    username: str
    access_token: str
