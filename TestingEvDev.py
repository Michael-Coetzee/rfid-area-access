from evdev.device import InputDevice
from evdev.util import categorize
from evdev import ecodes
import evdev
import sys


dev = InputDevice('/dev/input/event3')

keys = {
    2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 0,
}
card = ""
code = []
for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.value == 00:
            if event.code != 96:
                try:
                    code.append(keys[event.code])
                    if len(code) >= 10:
                        card = "".join(map(str, code))
                        print "Card scanned. tag ID:", card
                except:
                    code.append('')
                    code = []
                    card = ""

            

                    
            
