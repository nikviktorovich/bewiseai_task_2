import uuid

import audio_converter.common.errors


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()


def parse_uuid(hex: str) -> uuid.UUID:
    try:
        parsed_uuid = uuid.UUID(hex=hex)
    except ValueError:
        raise audio_converter.common.errors.BadUUIDError(
            f'Unable to parse UUID={hex}'
        ) from None
    else:
        return parsed_uuid
