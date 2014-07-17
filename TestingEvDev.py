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
<<<<<<< HEAD
                        card = ""
                        code = []
                        break
=======
                        # If card Is scannned agaIn code wIll append and gIve you a false value, cleanIng up needed
                        card = ""
                        code = []
>>>>>>> 857b2d8cb4bd53ca83193b188d066be25dac627d
                except:
                    code.append('')
            else:
                card = "".join(map(str, code))
                print card
                card = ""
                code = []


            

                    
            
