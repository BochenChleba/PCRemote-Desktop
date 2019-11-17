from dataclasses import dataclass


@dataclass
class WindowsCommands:

    SHUTDOWN_NOW = 'shutdown -s'  # -p
    SHUTDOWN_ABORT = 'shutdown -a'
    SCHEDULE_SHUTDOWN = 'shutdown -s -t '   # + time in seconds
    RESTART = 'shutdown -r -t 0'
