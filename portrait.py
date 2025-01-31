from gpiozero import MotionSensor
import sys
from omxplayer.player import OMXPlayer
from time import sleep
import json

with open('/home/pi/Videos/markers.json') as myfile:
    data = myfile.read()

obj = json.loads(data)

x = sys.argv[1]
y = sys.argv[2]
width = '1700'
height = '1100'
print("Starting up....")
tgr = 0
try:
    player = OMXPlayer('/home/pi/Videos/portraitsallhd.mp4',  args=['--no-osd', '--loop', '--win', '{0} {1} {2} {3}'.format(x, y, width, height)])
    pir = MotionSensor(4)
    sleep(1)
    print("Ready to trigger")
    #player.play()
    while True:
        player.pause()
        if pir.motion_detected:
            print('trigger count {}'.format(tgr))
            print('sleeping for {}'.format(obj[tgr]['duration']))
            player.play()
            sleep(obj[tgr]['duration'])
            print("Ready to trigger")
            tgr = tgr + 1
            if tgr < len(obj) : 
                player.set_position(obj[tgr]['start'])
            else:
                tgr = 0
                player.set_position(0)
        else:
            pass

except KeyboardInterrupt:
    player.quit()
    sleep(3)
    sys.exit()
