import socket

from constants import Constants
from serializer import Serializer
from communicator import Communicator
from windows_commands import WindowsCommands
from audio_controller import AudioController
import os


class Server:
    INTERNAL_COMMAND_SET_SHUTDOWN_TIMEOUT = False
    INTERNAL_COMMAND_SET_VOLUME_LEVEL = False
    audio_controller = AudioController()
    communicator = Communicator()

    def __init__(self):
        self.connection = self.init_connection()
        self.handle_connection()

    @staticmethod
    def init_connection():
        host = socket.gethostname()
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.bind((host, Constants.PORT_NR))
        return connection

    def handle_connection(self):
        self.start_listen()
        try:
            while True:
                command = self.communicator.receive_command()
                self.parse_command(command)
        except (ConnectionResetError, ConnectionAbortedError, TimeoutError) as e:
            self.handle_communication_error(e)

    def start_listen(self):
        self.connection.listen(1)
        client_socket, address = self.connection.accept()
        self.communicator.set_client_socket(client_socket)
        print("waiting for data...")

    def parse_command(self, command):
        if not command:
            print('no data, restarting...')
            raise ConnectionAbortedError

        elif self.INTERNAL_COMMAND_SET_SHUTDOWN_TIMEOUT:
            params = Serializer.deserialize_params(command)
            if len(params) == 1:
                os.system(WindowsCommands.SHUTDOWN_ABORT)
                os.system(WindowsCommands.SCHEDULE_SHUTDOWN + params[0])
                self.communicator.send_successful_response()
            else:
                self.communicator.send_unsuccessful_response()
            self.INTERNAL_COMMAND_SET_SHUTDOWN_TIMEOUT = False

        elif self.INTERNAL_COMMAND_SET_VOLUME_LEVEL:
            params = Serializer.deserialize_params(command)
            if len(params) == 1:
                level = int(params[0])
                self.audio_controller.set_volume(level)
                self.communicator.send_successful_response()
            else:
                self.communicator.send_unsuccessful_response()
            self.INTERNAL_COMMAND_SET_VOLUME_LEVEL = False

        elif command == Constants.COMMAND_PING:
            print("ping")
            self.communicator.send_successful_response([Constants.FEEDBACK_PONG])

        elif command == Constants.COMMAND_SHUTDOWN_NOW:
            print("shut system down")
            self.communicator.send_successful_response([])
            os.system(WindowsCommands.SHUTDOWN_NOW)

        elif command == Constants.COMMAND_SCHEDULED_SHUTDOWN:
            print("shut system down with timeout")
            self.communicator.send_awaiting_params_response()
            self.INTERNAL_COMMAND_SET_SHUTDOWN_TIMEOUT = True

        elif command == Constants.COMMAND_ABORT_SHUTDOWN:
            print("system shutdown aborted")
            self.communicator.send_successful_response()
            os.system(WindowsCommands.SHUTDOWN_ABORT)

        elif command == Constants.COMMAND_RESTART:
            print("system restart")
            self.communicator.send_successful_response()
            os.system(WindowsCommands.RESTART)

        elif command == Constants.COMMAND_SET_VOLUME:
            print("set volume")
            self.communicator.send_awaiting_params_response()
            self.INTERNAL_COMMAND_SET_VOLUME_LEVEL = True

        elif command == Constants.COMMAND_GET_VOLUME:
            print("get volume")
            current_volume = self.audio_controller.get_volume()
            self.communicator.send_successful_response([current_volume])

        #           elif data == NetworkConstants.COMMAND_DISCONNECT:
        #               print('Client requsted to disconnect. Disconnecting...')
        #               raise ConnectionAbortedError

    def handle_communication_error(self, error):
        pass
        print(str(error))
        print('Connection broken, waiting for host reconnection...')
        self.handle_connection()


if __name__ == '__main__':
    server = Server()

