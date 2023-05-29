from typing import BinaryIO

import pydub
import pydub.exceptions

import audio_converter.common.errors
from audio_converter.adapters.converter import abstract


class PydubAudioConverter(abstract.AudioConverter):
    def convert(self, input_stream: BinaryIO) -> BinaryIO:
        segment: pydub.AudioSegment
        
        try:
            segment = pydub.AudioSegment.from_wav(input_stream)
        except pydub.exceptions.CouldntDecodeError:
            raise audio_converter.common.errors.BadAudioFormatError(
            'Unable to decode the audio'
        ) from None

        return segment.export() # type: ignore
