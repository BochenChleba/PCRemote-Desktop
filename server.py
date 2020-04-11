import os
import socket

from audio_controller import AudioController
from communicator import Communicator
from constants import Constants
from keyboard_controller import KeyboardController
from message import Message
from mouse_controller import MouseController
from windows_commands import WindowsCommands


class Server:
    audio_controller = AudioController()
    communicator = Communicator()
    mouse_controller = MouseController()
    keyboard_controller = KeyboardController()

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
                message_str = self.communicator.receive_message()
                message = Message.from_string(message_str)
                self.read_message(message)
        except (ConnectionResetError, ConnectionAbortedError, TimeoutError) as e:
            self.handle_communication_error(e)

    def start_listen(self):
        self.connection.listen(1)
        client_socket, address = self.connection.accept()
        self.communicator.set_client_socket(client_socket)
        print("waiting for data...")

    def handle_communication_error(self, error):
        pass
        print(str(error))
        print('Connection broken, waiting for host reconnection...')
        self.handle_connection()

    def read_message(self, message):
        if not message.command:
            self.handle_empty_command()
        elif message.command == Constants.COMMAND_PING:
            self.handle_ping_command()
        elif message.command == Constants.COMMAND_SHUTDOWN_NOW:
            self.handle_shutdown_now_command()
        elif message.command == Constants.COMMAND_SCHEDULED_SHUTDOWN:
            self.handle_scheduled_shutdown_command(message.params)
        elif message.command == Constants.COMMAND_ABORT_SHUTDOWN:
            self.handle_abort_shutdown_command()
        elif message.command == Constants.COMMAND_RESTART:
            self.handle_restart_command()
        elif message.command == Constants.COMMAND_SET_VOLUME:
            self.handle_set_volume_command(message.params)
        elif message.command == Constants.COMMAND_GET_VOLUME:
            self.handle_get_volume_command()
        elif message.command == Constants.COMMAND_MUTE:
            self.handle_mute_command()
        elif message.command == Constants.COMMAND_UNMUTE:
            self.handle_unmute_command()
        elif message.command == Constants.COMMAND_MOUSE_MOVE:
            self.handle_mouse_move_command(message.params)
        elif message.command == Constants.COMMAND_MOUSE_LEFT_CLICK:
            self.handle_mouse_left_click_command()
        elif message.command == Constants.COMMAND_MOUSE_RIGHT_CLICK:
            self.handle_mouse_right_click_command()
        elif message.command == Constants.COMMAND_KEYBOARD_FETCH_KEY_STATE:
            self.handle_keyboard_fetch_state()
        elif message.command == Constants.COMMAND_KEYBOARD_SPECIAL_KEY:
            self.handle_keyboard_special_key_command(message.params)
        elif message.command == Constants.COMMAND_KEYBOARD_REGULAR_KEY:
            self.handle_keyboard_regular_key_command(message.params)
        else:
            self.handle_unknown_command()

    @staticmethod
    def handle_empty_command():
        print('no data, restarting...')
        raise ConnectionAbortedError

    def handle_unknown_command(self):
        print('unknown command')
        self.communicator.send_unsuccessful_response()

    def handle_ping_command(self):
        print("ping")
        self.communicator.send_successful_response([Constants.FEEDBACK_PONG])

    def handle_shutdown_now_command(self):
        print("shut system down")
        self.communicator.send_successful_response()
        os.system(WindowsCommands.SHUTDOWN_NOW)

    def handle_scheduled_shutdown_command(self, params):
        print("shut system down with timeout")
        if len(params) == 1:
            os.system(WindowsCommands.SHUTDOWN_ABORT)
            os.system(WindowsCommands.SCHEDULE_SHUTDOWN + params[0])
            self.communicator.send_successful_response()
        else:
            self.communicator.send_unsuccessful_response()

    def handle_abort_shutdown_command(self):
        print("system shutdown aborted")
        self.communicator.send_successful_response()
        os.system(WindowsCommands.SHUTDOWN_ABORT)

    def handle_restart_command(self):
        print("system restart")
        self.communicator.send_successful_response()
        os.system(WindowsCommands.RESTART)

    def handle_set_volume_command(self, params):
        print("set volume")
        if len(params) == 1:
            level = int(params[0])
            self.audio_controller.set_volume(level)
            self.communicator.send_successful_response()
        else:
            self.communicator.send_unsuccessful_response()

    def handle_get_volume_command(self):
        print("get volume")
        current_volume = self.audio_controller.get_volume()
        is_muted = self.audio_controller.is_muted()
        self.communicator.send_successful_response([current_volume, is_muted])

    def handle_mute_command(self):
        print("mute")
        self.audio_controller.mute()
        self.communicator.send_successful_response()

    def handle_unmute_command(self):
        print("unmute")
        self.audio_controller.unmute()
        self.communicator.send_successful_response()

    def handle_mouse_move_command(self, params):
        print("mouse move")
        if len(params) == 2:
            x_offset = float(params[0])
            y_offset = float(params[1])
            self.mouse_controller.move(x_offset, y_offset)
        self.communicator.send_successful_response()

    def handle_mouse_left_click_command(self):
        print("mouse left click")
        self.mouse_controller.left_click()
        self.communicator.send_successful_response()

    def handle_mouse_right_click_command(self):
        print("mouse right click")
        self.mouse_controller.right_click()
        self.communicator.send_successful_response()

    def handle_keyboard_special_key_command(self, params):
        print("keyboard key")
        if len(params) == 1:
            key = params[0]
            self.keyboard_controller.press_special_key(key)
        self.communicator.send_successful_response()

    def handle_keyboard_regular_key_command(self, params):
        print("keyboard key regular")
        if len(params) == 1:
            key = params[0]
            self.keyboard_controller.writeChar(key)
        self.communicator.send_successful_response()

    def handle_keyboard_fetch_state(self):
        print("keyboard fetch state")
        state = self.keyboard_controller.get_keys_state()
        self.communicator.send_successful_response([state])

if __name__ == '__main__':
    server = Server()

