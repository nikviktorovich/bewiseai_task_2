import dataclasses
import uuid
from typing import Any


@dataclasses.dataclass
class User:
    id: Any
    username: str
    access_token: uuid.UUID
