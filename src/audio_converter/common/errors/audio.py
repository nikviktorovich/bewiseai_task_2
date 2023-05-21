class AudioError(Exception):
    """Base class for all audio exceptions"""


class BadAudioFormatError(AudioError):
    """Bad audio format error"""
