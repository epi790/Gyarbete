import keys
from masterkey import masterkey
import qrreader
import sqlite3
import time
import base64
import ast
import serial

arduino_port = '/dev/ttyACM0' 
database = sqlite3.connect("rudbeck.db")
cursor = database.cursor()
ser = serial.Serial(arduino_port, 9600, timeout=1)


def send_light(color):
    ser.write(color.encode())
    time.sleep(2)


def get_key_from_name(name):
   
    query = f'select sharedkey from shared where name is "{name}";'
    
    cursor.execute(query)
    result = cursor.fetchone()

    if result is None:
        return False

    result = base64.b64decode(ast.literal_eval(result[0]))
    return result


vs = qrreader.init()

while True:
    

    result = qrreader.get_qr_data(vs)

    if result == None:
        time.sleep(0.5)
        continue

    try:
        
        key_pem, name = result.split(",")

        key_pem = base64.b64decode(ast.literal_eval(key_pem))
        name = name.replace(' ', '')
        
    except:
        print("Unrecognized format")
        send_light("R")
        time.sleep(0.5)
        continue
 
    if key_pem and name is not None:
        if get_key_from_name(name):
            sharedkey = get_key_from_name(name)
        else:
            print("User not in databse")
            send_light("R")
            #time.sleep(0.5)
            continue

        if sharedkey == None:
            time.sleep(0.5)
            continue
      
        key_now = keys.derive_new_key_from_time(sharedkey)

        if key_now == key_pem: 
            print("welcome")
            send_light("G")
            
        else:
            print("NUH UH ")
            send_light("R")
    time.sleep(1)
            
