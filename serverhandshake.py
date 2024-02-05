import keys
from masterkey import masterkey
import qrreader
import sqlite3
from time import sleep
from base64 import b64decode, b64encode
import ast

database = sqlite3.connect("rudbeck.db")
cursor = database.cursor()


def get_name_from_key(key_pem):
    query = f'select name from users where key is "{key_pem}";'
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def give_access():
    return 1


def adduser(name, shared_key):
    shared_key = b64encode(shared_key)
    query = f'insert or ignore into shared VALUES("{name}", "{shared_key}")'
    cursor.execute(query)
    database.commit()


vs = qrreader.init()
name = ""

while True:

    result = qrreader.get_qr_data(vs)
    if result == None:
        sleep(0.5)
        continue

    else:
        print(result)
        key_pem, name = result.split(",")
        key_pem = key_pem.encode()
        print(f"pem: {key_pem}")
        print()
        print(f"name: {type(key_pem)}")
        sharedkey = keys.generate_shared_key(keys.private_pem_to_key(
            masterkey), keys.public_pem_to_key(key_pem))
        adduser(name, sharedkey)
        exit()

    sleep(1)
