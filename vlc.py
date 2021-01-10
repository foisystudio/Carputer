from gpiozero import LED
from gpiozero import Button
from picamera import PiCamera
from time import sleep
from datetime import datetime
from signal import pause
from subprocess import check_call

vlc = Button(17)

def vlc_start():
    check_call(['vlc', '/home/pi/Music/playlist1.xspf'])

while True:
    vlc.when_pressed = vlc_start
    pause()
