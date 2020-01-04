import pyautogui


class MouseController:
    MOVE_FACTOR = 4000

    def __init__(self):
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0.01

    def move(self, x_offset: float, y_offset: float):
        pyautogui.move(x_offset * self.MOVE_FACTOR, y_offset * self.MOVE_FACTOR)
