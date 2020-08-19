# PCRemote-Desktop
Desktop part of communication system, which allows to control Windows PC behavior with Android mobile device. User can shutdown system, change system volume, control mouse movement and use keyboard input. It establishes connection between devices over Wifi network.

[Video presentation](https://youtu.be/zZzGG5zplpQ)

Communication system consists of two applications: mobile, which can be found [here](https://github.com/BochenChleba/PCRemote-Mobile) and PC (this app).

Features:
  - Shutting down and rebooting Windows. Command can be executed right away or at specifited time.
  - System volume level change. Muting and unmuting.
  - Mouse movement control, left and right mouse buttons clicks.
  - Keyboard input.
  - Wifi network scan searching for target PC.

Requirements:
  - Android device with [mobile-side application](https://github.com/BochenChleba/PCRemote-Mobile) installed.
  - Mobile and PC devices should be connected to the same Wifi network.
  - Python 3 installed on PC machine.
  
Launching:
  - make sure that desktop and mobile machines are connected to the same Wifi network.
  - run python command in Windows CMD passing path to server.py file as an argument.
  - launch mobile application on mobile device.
  - connect devices by Wifi scan or by manually entering Ip address of desktop machine on mobile device.
