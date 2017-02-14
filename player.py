import RPi.GPIO as GPIO
from omxplayer import OMXPlayer as omx
import sys
from time import sleep

vid = sys.argv[0]
omxargs = sys.argv[1:]

try:

    video = omx(vid, args = omxargs, pause=True)

    GPIO.setmode(GPIO.BCM)

    GPIO.setwarnings(False)

    PLAY = 17
    PAUSE = 27
    STOP = 22
    RESET = 5

    GPIO.setup(PLAY, GPIO.IN)
    GPIO.setup(PAUSE, GPIO.IN)
    GPIO.setup(STOP, GPIO.IN)
    GPIO.setup(RESET,  GPIO.IN)

    wait = True

    while True:
        while wait:

            if(GPIO.input(PLAY) == False):
                video.play()
                wait = False

        while not wait:
            if GPIO.input(PAUSE) == False:
                video.pause()
                wait = True

            if GPIO.input(STOP) == False:
                video.set_position(0)
                video.pause()
                wait = True

            if GPIO.input(RESET) == False:
	        video.quit()
                video = omx(vid, args = omxargs, pause=True)
                wait = True

except KeyboardInterrupt:
    video.stop()
    print "Bye"





