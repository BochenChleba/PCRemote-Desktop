from aenum import MultiValueEnum


class KeyboardKey(MultiValueEnum):
    KEY_ESC = 0, "esc"
    KEY_TAB = 1, "tab"
    KEY_SHIFT = 2, "shift"
    KEY_CTRL = 3, "ctrl"
    KEY_WINDOWS = 4, "windows"
    KEY_ALT = 5, "alt"
