import time
import RPi.GPIO as GPIO
import requests
from threading import Thread

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

runtimeArr = []

GPIO.setup(4, GPIO.IN)  # Moisture Sensor
GPIO.setup(22, GPIO.IN)  # Switch
GPIO.setup(18, GPIO.OUT)  # Buzzer / LED
GPIO.setup(24, GPIO.OUT)  # Buzzer / LED

print('It is not raining :)')


def sendAlert():

    bot_token = '1633948097:AAEr1VWwO099l2dDRWhVh1Ch898BrJ8MIVg'

    # chatID have to change based on who u want the bot to send msg to
    # you have to go to telegram and search for this bot "IOT_rainalertBot"
    # then press the start button
    # in a browser, open this link https://api.telegram.org/bot1633948097:AAEr1VWwO099l2dDRWhVh1Ch898BrJ8MIVg/getUpdates
    # you should see like some json format data, and it should have ur username
    # you need to replace the chatID here with the id from the json data

    bot_chatID = '418787867'
    alertMsg = 'Alert!! raining'

    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + alertMsg

    response = requests.get(send_text)

    return response.json()


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
    GPIO.output(18, 1)
    GPIO.output(24, 1)
    time.sleep(3)
    GPIO.output(18, 0)
    GPIO.output(24, 0)


def moistureLoop():
    while True:
        if moistureCheck() == True:
            print("Alert to phone")
            sendAlert()
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
    MATRIX = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9],
              ['*', 0, '#']]  # layout of keys on keypad

    ROW = [6, 20, 19, 13]  # row pins
    COL = [12, 5, 16]  # column pins

    # set column pins as outputs, and write default value of 1 to each
    for i in range(3):
        GPIO.setup(COL[i], GPIO.OUT)
        GPIO.output(COL[i], 1)

    # set row pins as inputs, with pull up
    for j in range(4):
        GPIO.setup(ROW[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # scan keypad
    while len(runtime) <= 5:
        for i in range(3):  # loop thru’ all columns
            GPIO.output(COL[i], 0)  # pull one column pin low
            for j in range(4):  # check which row pin becomes low
                if GPIO.input(ROW[j]) == 0:  # if a key is pressed
                    runtime += str(MATRIX[j][i])
                    if len(runtime) == 4:
                        runtime = runtime[:2] + ':' + runtime[2:]
                        runtimeArr.append(runtime)
                        print(runtimeArr)

                        # thingspeak cloud upload
                        print(f'{"":-^40}')
                        print(f'{"Uploading data...": ^40}')
                        resp = requests.get(
                            "https://api.thingspeak.com/update?api_key=KYZKACCC3QKGA5XM&field1=%s&field2=%s" % (time.strftime("%d-%m-%Y"), runtime))
                        print(
                            f'Runtime: {runtime}, Date: {time.strftime("%d/%m/%Y")}')
                        print(f'{"":-^40}')

                        runtime = ''
                    while GPIO.input(ROW[j]) == 0:  # debounce
                        time.sleep(0.1)
            GPIO.output(COL[i], 1)  # write back default value of 1


thread1 = Thread(target=moistureLoop)
threads = [thread1]
thread2 = Thread(target=inputLoop)
threads += [thread2]

thread1.start()
thread2.start()

for tloop in threads:
    tloop.join()
