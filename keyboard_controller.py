import keyboard
import json
from constants import Constants

INDEX_OF_KEY_COMMAND = 1


class KeyboardController:

    keys_state = {Constants.KEY_SHIFT: False, Constants.KEY_CTRL: False, Constants.KEY_ALT: False}

    def press_special_key(self, key: str):
        if self.keys_state.__contains__(key):
            self.__press_or_release_key(key)
        else:
            self.press_and_release_key(key)

    def __press_or_release_key(self, key: str):
        is_pressed = self.keys_state[key]
        if is_pressed:
            keyboard.release(key)
        else:
            keyboard.press(key)
        self.keys_state[key] = not is_pressed
        print("Key ", key, "is pressed - ", not is_pressed)
        print(repr(self.keys_state))

    @staticmethod
    def press_and_release_key(key: str):
        keyboard.press_and_release(key)
        print("Key ", key, "is pressed and released ")

    @staticmethod
    def writeChar(key: str):
        keyboard.write(key)
        print("Key ", key, " written")

    def get_keys_state(self):
        return json.dumps(self.keys_state)
