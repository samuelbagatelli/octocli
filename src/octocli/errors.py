from enum import IntEnum


class ErrorCode(IntEnum):
    SUCCESS = 0
    FILE_NOT_FOUND = 2
    ACCESS_DENIED = 5
    UNKNOWN_ERROR = 127
