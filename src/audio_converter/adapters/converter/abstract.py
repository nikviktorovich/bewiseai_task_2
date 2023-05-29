from typing import BinaryIO


class AudioConverter:
    def convert(self, input_stream: BinaryIO) -> BinaryIO:
        raise NotImplementedError()
