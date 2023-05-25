import uuid


class AbstractUUIDProvider:
    def parse(self, hex_uuid: str) -> uuid.UUID:
        raise NotImplementedError()
    

    def generate(self) -> uuid.UUID:
        raise NotImplementedError()
