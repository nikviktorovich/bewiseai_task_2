import uuid

from . import abstract


class DefaultUUIDProvider(abstract.UUIDProvider):
    def parse(self, hex_uuid: str) -> uuid.UUID:
        return uuid.UUID(hex=hex_uuid)
    

    def generate(self) -> uuid.UUID:
        return uuid.uuid4()
