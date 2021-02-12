import time
import requests
from threading import Thread

runtimeArr = []

print(f'{"":-^40}')
print(f'{"It is not raining :)": ^40}')

def moistureCheck():
    if input("Moisture check y/n?\n>> ") == "y":
        return True
    else:
        return False

def switchCheck():
    if input("Switch check y/n?\n>> ") == "y":
        return True
    else:
        return False

def buzzerAlert():
    print(f'{"":-^40}')
    print(f'{"BUZZER ON": ^40}')
    print(f'{"LED ON": ^40}')
    time.sleep(3)
    print(f'{"":-^40}')
    print(f'{"After 3 sec...": ^40}')
    print(f'{"":-^40}')
    print(f'{"BUZZER OFF": ^40}')
    print(f'{"LED OFF": ^40}')

def moistureLoop():
    while True:
        stopLoop = input("Do you want to stop testing moisture loop? y/n\n>> ")
        if stopLoop == "y":
            break
        else:
            if moistureCheck() == True:
                print(f'{"":-^40}')
                print("Alert to phone")
                print("It is raining :(")
                print(f'{"":-^40}')
                if switchCheck() == True:
                    buzzerAlert()
                time.sleep(10)
                print(f'{"After 10 min...": ^40}')
                print(f'{"":-^40}')
                while moistureCheck() == True:
                    time.sleep(10)
                    print(f'{"After 2 min...": ^40}')
                print('It is not raining :)')
                continue
            else:
                continue

def inputLoop():
    runtime = ''

    while len(runtime) <= 5:
        print(f'{"":-^40}')
        runtime = input("User runtime?\n >> ")
        if len(runtime) == 4:
            runtime = runtime[:2] + '.' + runtime[2:]
            runtimeArr.append(runtime)
            print(f'{"":-^40}')
            print(runtimeArr)
            print(f'{"":-^40}')
            print(f'{"Uploading data...": ^40}')
            resp = requests.get("https://api.thingspeak.com/update?api_key=KYZKACCC3QKGA5XM&field1=%s&field2=%s" %(time.strftime("%d-%m-%Y"), runtime))
            print(f'Runtime: {runtime}, Date: {time.strftime("%d-%m-%Y")}')
            print(f'{"":-^40}')
            runtime = ''
        testRuntime = input("U want to test the runtime loop? y/n\n>> ")
        if testRuntime == "n":
            break

while True:
    print(f'{"":-^40}')
    endProg = input("End program? y/n\n>> ")
    if endProg == "y":
        break

    moistureLoop()
    testRuntime = input("U want to test the runtime loop? y/n\n>> ")
    if testRuntime == "y":
        inputLoop()