from constants import Constants
from serializer import Serializer


class Communicator:
    def __init__(self):
        self.client_socket = None

    def set_client_socket(self, client_socket):
        self.client_socket = client_socket

    def send_successful_response(self, params: list = None):
        if params is None:
            params = []
        self.client_socket.sendall(bytearray(
            Serializer.serialize_response(Constants.FEEDBACK_SUCCEED, params),
            Constants.ENCODING
        ))

    def send_unsuccessful_response(self, params: list = None):
        if params is None:
            params = []
        self.client_socket.sendall(bytearray(
            Serializer.serialize_response(Constants.FEEDBACK_FAILED, params),
            Constants.ENCODING
        ))

    def receive_message(self):
        return self.client_socket.recv(Constants.DATA_BUFFER_SIZE).decode(Constants.ENCODING)
