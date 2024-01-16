import keys
from masterkey import masterkey
import qrreader
import sqlite3
import time
import base64

print(masterkey)

database = sqlite3.connect("rudbeck.db")
cursor = database.cursor()


def get_key_from_name(name):
    query = f'select sharedkey from shared where name is "{name}";'
    cursor.execute(query)
    result = cursor.fetchone()
    print(result)
    result = base64.b16decode(result[0])
    print("\n"*3)
    print(result)
    return result

def give_access():
    print("IS HAS ARRIVED AAAAAAAAAAAAAAAAAAAAAAAa")
    return True


vs = qrreader.init()

#cursor.execute(query)
result = cursor.fetchall()


#key_pem = r'''-----BEGIN PRIVATE KEY-----\nMIG2AgEAMBAGByqGSM49AgEGBSuBBAAiBIGeMIGbAgEBBDDGokHL9IFveoU/i65P\nnzySq4xD8W3AyMwaLaDzvWMNIeD1Y4kI2w0mrJdZiybDWkGhZANiAAQL0+j9MKuY\nminc5M8saSfAxBeycBUZw/8PcqO+L33CeVDldefAc1drDkfc+ZUBcaSR4QeioQno\nuQXFqRayv4IpzhPwod/NE04CyWlCtee9XrZa7qSPlgWYM37QivJWml0=\n-----END PRIVATE KEY-----'''
#query = f"select name from users where key is {key_pem}"
name = ""

while True:

    result = qrreader.get_qr_data(vs)
    if result == None:
        continue

    key_pem, name = result.split(",")

    if key_pem and name is not None:
        sharedkey = get_key_from_name(name)
        print("\n"*3)
        
        print(sharedkey)
        

        if keys.derive_new_key_from_time(sharedkey) == key_pem:
            give_access()
            
    print(result) 
    time.sleep(1)


