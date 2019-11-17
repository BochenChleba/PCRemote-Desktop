from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class AudioController:
    PERCENT_FACTOR = 100

    def __init__(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))

    def get_volume(self):
        return round(self.volume.GetMasterVolumeLevelScalar() * self.PERCENT_FACTOR)

    def set_volume(self, level):
        if level > 100 or level < 0:
            raise Exception("invalid volume level")
        self.volume.SetMasterVolumeLevelScalar(level / self.PERCENT_FACTOR, None)

