import time
from multiprocessing import Process

print('It is not raining :)')

def moisturecheck():
    return True
    # return False

    #  insert way to check pin here
    # True = Wet
    # False = Dry

def buzzercheck():
    return True
    # return False

    # insert way to check if switch is on or off
    # True = on
    # False = off

def keypadcheck(): 
    # return True
    return False

    # Checks if keypad is pressed
    # True = pressed
    # False = nothing

def moistureloop():
    while True:
        if moisturecheck() == True:
            print("Alert to phone")
            print("It is raining :(")
            if buzzercheck() == True:
                print('Buzzer on')
                print('LED on')
                time.sleep(6)
                print('Buzzer off')
                print('LED off')
            time.sleep(10)
            print("10min")
            while moisturecheck() == True:
                time.sleep(10)
                print("2min")
            print('checkkIt is not raining :)')
            continue
        else:
            continue

def inputloop():
    while True:
        if keypadcheck() == True:
            x = input("Please input your time: ")
            print("Send to cloud")
            continue


if __name__ == '__main__':
    time.sleep(1)
    Process(target=moistureloop).start()
    time.sleep(1)
    Process(target=inputloop).start()