from dataclasses import dataclass


@dataclass
class Constants:

    PORT_NR: int = 8081
    DATA_BUFFER_SIZE = 64

    COMMAND_PING: str = "0"
    COMMAND_SHUTDOWN_NOW: str = "1"
    COMMAND_SCHEDULED_SHUTDOWN: str = "2"
    COMMAND_ABORT_SHUTDOWN: str = "3"
    COMMAND_RESTART = "4"
    COMMAND_SET_VOLUME = "5"
    COMMAND_GET_VOLUME = "6"
    FEEDBACK_AWAITING_PARAMS: str = "ready"
    FEEDBACK_SUCCEED: str = "ok"
    FEEDBACK_FAILED: str = "failed"
    FEEDBACK_PONG: str = "pong"
    FEEDBACK_VOLUME_LEVEL: str = "volume"

    SEPARATOR = '&'
    ENCODING = 'utf-8'
