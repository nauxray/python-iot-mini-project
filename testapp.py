import time
import requests
from threading import Thread

from telethon.sync import TelegramClient 
from telethon.tl.types import InputPeerUser, InputPeerChannel 
from telethon import TelegramClient

api_id = '2616181'
api_hash = 'a2c456736c48db4a64cf944634eaf3c4'
token = '1582053448:AAFSoZpF0i5TWq3ECP0sBtI6apabD5C02so'
runtimeArr = []

phone = '+65' + input("Enter phone number (yx is 92973342): ")
print("PHONE NUMBER:", phone)

print(f'{"":-^40}')
print(f'{"It is not raining :)": ^40}')

def sendMsg():
    # creating a telegram session and assigning 
    # it to a variable client 
    client = TelegramClient('session', api_id, api_hash) 
    
    # connecting and building the session 
    client.connect() 
    
    # in case of script ran first time it will ask either to input token or otp sent to number or sent or your telegram id  
    if not client.is_user_authorized(): 
        client.send_code_request(phone) 
        # signing in the client 
        client.sign_in(phone, input('Enter the code: ')) 
    try: 
        # melvin's userinfo inserted to send msg to him
        receiver = InputPeerUser(client.get_entity("BobaSucker").id, client.get_entity("BobaSucker").access_hash)     
        # sending message using telegram client 
        client.send_message(receiver, "ALERT ALERT", parse_mode='html') 
    except Exception as e: 
        print(e);     
    # disconnecting the telegram session  
    client.disconnect() 


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
        stopLoop = input("Stop testing moisture loop? y/n\n>> ")
        if stopLoop == "y":
            break
        else:
            if moistureCheck() == True:
                print(f'{"":-^40}')
                print("Alert to phone")
                sendMsg()
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
        testRuntime = input("Test the runtime loop? y/n\n>> ")
        if testRuntime == "n":
            break

while True:
    print(f'{"":-^40}')
    endProg = input("End program? y/n\n>> ")
    if endProg == "y":
        break

    moistureLoop()
    testRuntime = input("Test the runtime loop? y/n\n>> ")
    if testRuntime == "y":
        inputLoop()