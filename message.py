from constants import Constants


class Message:
    command: str
    params: tuple

    def __init__(self, command: str, params: tuple):
        self.command = command
        self.params = params

    @staticmethod
    def from_string(message_string: str):
        received_data = tuple(message_string.split(Constants.SEPARATOR))
        return Message(received_data[0], received_data[1:])
