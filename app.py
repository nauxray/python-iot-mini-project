import time
import RPi.GPIO as GPIO 
import requests
from threading import Thread

GPIO.setmode(GPIO.BCM)  
GPIO.setwarnings(False)

runtimeArr = []

GPIO.setup(4, GPIO.IN) # Moisture Sensor
GPIO.setup(22, GPIO.IN) # Switch
GPIO.setup(18, GPIO.OUT) # Buzzer / LED
GPIO.setup(24, GPIO.OUT) # Buzzer / LED

print('It is not raining :)')

def moistureCheck():
    if GPIO.input(4):
        return True
    else:
        return False

def switchCheck():
    if GPIO.input(22):
        return True
    else:
        return False

def buzzerAlert():
    GPIO.output(18,1)
    GPIO.output(24,1)
    time.sleep(3)
    GPIO.output(18,0)
    GPIO.output(24,0)

def moistureLoop():
    while True:
        if moistureCheck() == True:
            print("Alert to phone")
            print("It is raining :(")
            if switchCheck() == True:
                buzzerAlert()
            time.sleep(10)
            print("10min")
            while moistureCheck() == True:
                time.sleep(10)
                print("2min")
            print('It is not raining :)')
            continue
        else:
            continue

def inputLoop():
    runtime = ''
    MATRIX=[[1,2,3],
            [4,5,6],
            [7,8,9],
            ['*',0,'#']] #layout of keys on keypad

    ROW=[6,20,19,13] #row pins
    COL=[12,5,16] #column pins

    #set column pins as outputs, and write default value of 1 to each
    for i in range(3):
        GPIO.setup(COL[i],GPIO.OUT)
        GPIO.output(COL[i],1)

    #set row pins as inputs, with pull up
    for j in range(4):
        GPIO.setup(ROW[j],GPIO.IN,pull_up_down=GPIO.PUD_UP)

    #scan keypad
    while len(runtime) <= 5:
        for i in range(3): #loop thru’ all columns
            GPIO.output(COL[i],0) #pull one column pin low
            for j in range(4): #check which row pin becomes low
                if GPIO.input(ROW[j])==0: #if a key is pressed
                    runtime += str(MATRIX[j][i])
                    if len(runtime) == 4:
                        runtime = runtime[:2] + ':' + runtime[2:]
                        runtimeArr.append(runtime)
                        print(runtimeArr)
                        runtime = ''
                    while GPIO.input(ROW[j])==0: #debounce
                        time.sleep(0.1)
            GPIO.output(COL[i],1) #write back default value of 1

thread1 = Thread(target=moistureLoop)
threads = [thread1]
thread2 = Thread(target=inputLoop)
threads += [thread2]

thread1.start()
thread2.start()

for tloop in threads:
    tloop.join()