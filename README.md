/* rfid2.py - simple rfid reader that logs to DB on raspberry pi
 *
 * Michael Coetzee <michaelcoetzee146@gmail.com>
 * 
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

raspberry pi +  usb rfid reader + sqlite3 + python

code to read data fron cheap usb card reader:
http://www.ebay.com/itm/USB-RFID-ID-Contactless-Proximity-Smart-Card-Reader-EM4001-EM4100-Windows-/261356847082
for $3.99 as of 08/07/2014

You will need:
              above mentioned card
              raspberry pi
              sd card
              if you have a monitor that supports hdmi, well done!
              if not, im using a hdmi to vga convertor:
              https://www.modmypi.com/pi-vew-raspberry-pi-hdmi-to-vga-converter
              breadboard
              1k0 resistors
              LED's RED, GREEN, BLUE
              network cable
              usb hub
              keyboard 
              mouse

Ok, first i Created a sqlite3 database called areaDatabase that stored 3 tables called rfid, rejected, tracker,
inside rfid i stored data that python code would call to fetch to verify whether tag exists, inside rejected 
if tag id does not exist it will log to rejected, inside tracker everytime the tag is read it will log to tracker.

once the code is executed a blue light will turn on stating that the reader will now accept incoming data from reader,
if a card is swiped and the tag id is verified against the database is accepted, a green LED will switch on for two seconds
reverting back to default blue, if tag id is not accepted a red led will switch on for two seconds also the false tag id 
will be recorded onto database.

that is basically it for now, i want continously modify and tweek project to oneday accept two card readers and only accept
one tag swipe at a time untill tag has been swiped at second reader, for future in and out purposes.
              
              

