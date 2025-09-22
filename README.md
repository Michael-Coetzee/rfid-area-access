/* USB RFID readers, using a Raspberry Pi, that logs into a sqlite DB.
 *
 * Michael Coetzee <michaelcoetzee146@gmail.com>
 * 
 * This code is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This code is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 */


rfid-area-access
================

Raspberry Pi +  USB RFID reader + sqlite3 + python 2.7

code to read data fron cheap usb card reader:
http://www.ebay.com/itm/USB-RFID-ID-Contactless-Proximity-Smart-Card-Reader-EM4001-EM4100-Windows-/261356847082
for $3.99 as of 08/07/2014

You will need:

above mentioned cards,
Raspberry Pi,
sd card,
if you have a monitor that supports hdmi, well done!
if not, im using a hdmi to vga convertor:
https://www.modmypi.com/pi-vew-raspberry-pi-hdmi-to-vga-converter,
breadboard,
1k0 resistors,
LED's RED, GREEN, BLUE,
network cable,
usb hub,
keyboard, 
mouse

=====================================================================================================================

Ok, first we create a sqlite3 database called areaDatabase.db that stored 3 tables called employee, rejected and tracking.
Inside tracking, the card number(s) that has been previously loaded into database will be called upon to check whether card 
exists and then updated according to where card user is situated geologically, entry/exit.
Inside rejected, if tag id does not exist, card number will stored into rejected(for future use: maybe a supervisor override). 
Inside tracking everytime the tag is read it will check to see whether card is in an exit state or entry state, and depending
on which state the card user is in, it will update accordingly.

Once the code is run for the first time a blue light will turn on stating that the reader will now accept incoming data from reader,
if a card is swiped and the tag id is verified against the database and is accepted, a green LED will switch on for two seconds
reverting back to default blue, if tag id is not accepted a red led will switch on for two seconds once again reverting back 
to the default blue

That is basically it for now, i want continously modify and tweak project to one day accept data from two card readers only,
and accept one tag swipe at a time untill tag has been swiped at second reader, for future in and out purposes.

Update... managed to get rid of raw_input which in my opinion is not secure, we have implemented the 'evdev' lib,
and now it will accept data from the RFID readers only. Once card is read it will allow entry or exit(depending on user location),
if card is read a second time at the same device it will not allow entry or exit untill card is read at second device. 
Thus if an electronic latch is installed it will only trigger when user has scanned in or out only.

Added a png drawing of the LED setup using Fritzing.

So i think we could expand on this project a little more... maybe a relay for a door, biometric fingerprint scanner 
for more secure area's of the building, iris scanner, facial recognition, anti loitering scanner... the possibilities are endless.
:) 
              
