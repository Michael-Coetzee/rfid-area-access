import time, sys
import sqlite3 as lite
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GREEN_LED = 18
BLUE_LED = 24
RED_LED = 23
GPIO.setup(BLUE_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
# link to database
con = lite.connect('areaDatabase.db')
# connect to DB
cur = con.cursor()              

#create tables if they do not exist
cur.execute('CREATE TABLE IF NOT EXISTS employee (ID INTEGER PRIMARY KEY, Card TEXT, Name TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS tracking (ID INTEGER PRIMARY KEY, Card TEXT, Date DATETIME, Status INTEGER DEFAULT 0)')
cur.execute('CREATE TABLE IF NOT EXISTS rejected (ID INTEGER PRIMARY KEY, Card TEXT, Date TEXT)')
#example code: remove when in real world application just for testing purposes
cur.execute('REPLACE INTO employee values(0001, "121743110", "Jack Aranda")')
cur.execute('REPLACE INTO employee values(0002, "121723560", "Cherry Blossom")')
cur.execute('REPLACE INTO employee values(0003, "121741279", "Olive Tree")')

GPIO.output(BLUE_LED, True)
try:
    while True:
        # loop until tag is read
        thetime = time.strftime("%Y-%m-%d %a %H:%M:%S", time.localtime())
        # read data from rfid
        rfid_data = raw_input().strip()
        # check data
        if  len(rfid_data) > 0:
            # only get tag number
            rfid_data = rfid_data[1:11]
            # print number
            print "Card Scanned. Tag ID:", rfid_data  
            cur.execute("SELECT Card, Name FROM employee WHERE Card = ?", [rfid_data])
            # fetch name of card holder if exists
            employee = cur.fetchone()
            # if card not found execute the following code
            if not employee:                
                GPIO.output(BLUE_LED, False)
                GPIO.output(RED_LED, True)
                time.sleep(2)
                GPIO.output(RED_LED, False)
                GPIO.output(BLUE_LED, True)
                print "UNAUTHORIZED CARD! [",rfid_data,"] scanned at area @ ",thetime
                # logging unauthorised card into database
                cur.execute("INSERT INTO rejected (Card, Date) VALUES(?,?)", (rfid_data, thetime))
                con.commit()                
                continue
                # if card found execute the following
            else:                           
                GPIO.output(BLUE_LED, False)
                GPIO.output(GREEN_LED, True)
                time.sleep(2)
                GPIO.output(GREEN_LED, False)
                GPIO.output(BLUE_LED, True)
                print "Card found in DB."

                # get last record for card
                cur.execute("SELECT Status FROM tracking WHERE Card = ? ORDER BY datetime(Date) DESC LIMIT 1", [employee[0]])
                employeeStatus = cur.fetchone()

                if not employeeStatus or employeeStatus[0] == 0:
                    cur.execute("INSERT INTO tracking (Card, Date, Status) VALUES(?,?,?)", (rfid_data, time.time(), 1))
                    print employee[1],"entered area @", thetime
                elif employeeStatus[0] == 1:
                    cur.execute("INSERT INTO tracking (Card, Date, Status) VALUES(?,?,?)", (rfid_data, time.time(), 0))
                    print employee[1],"left area @", thetime

                # commit changes to database 
                con.commit()

except KeyboardInterrupt:
    print "Caught interrupt, exiting..."
    print "Unexpected error:", sys.exc_info()[0]
    raise
finally:
    # close connection
    cur.close()
     # cleanup GPIO
    GPIO.cleanup()                        
