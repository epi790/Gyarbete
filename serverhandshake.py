import keys
from masterkey import masterkey
import qrreader
import sqlite3
import time
import base64

#print(masterkeypem)

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
    print("CALlEd")
    print(f"{name},{shared_key})")
    query = f'insert into shared VALUES("{name}", "{shared_key.decode()}")'
    #query = 'insert into shared values("foo", "bar");'
    print(query)
    cursor.execute(query)
    database.commit()



vs = qrreader.init()

#cursor.execute(query)
result = cursor.fetchall()


#key_pem = r'''-----BEGIN PRIVATE KEY-----\nMIG2AgEAMBAGByqGSM49AgEGBSuBBAAiBIGeMIGbAgEBBDDGokHL9IFveoU/i65P\nnzySq4xD8W3AyMwaLaDzvWMNIeD1Y4kI2w0mrJdZiybDWkGhZANiAAQL0+j9MKuY\nminc5M8saSfAxBeycBUZw/8PcqO+L33CeVDldefAc1drDkfc+ZUBcaSR4QeioQno\nuQXFqRayv4IpzhPwod/NE04CyWlCtee9XrZa7qSPlgWYM37QivJWml0=\n-----END PRIVATE KEY-----'''
#query = f"select name from users where key is {key_pem}"
name = ""

print("start loop")
while True:

    result = qrreader.get_qr_data(vs)
    if result == None:
        continue

    else:
        print(result)
    
    for i in result:
        if i == ",":
            key_pem, name = result.split(",")
            print(key_pem)
            #key_pem = key_pem.replace('\'', "")[1:]
            #print(key_pem)
            print(key_pem.encode())
            print("CAllING...")
            #print(keys.generate_shared_key_pem(keys.private_pem_to_key(masterkey), keys.public_pem_to_key(key_pem.encode())))
            adduser(name, base64.b16encode(keys.generate_shared_key(keys.private_pem_to_key(masterkey), keys.public_pem_to_key(key_pem.encode()))))
            exit()

    #print(result) 
    time.sleep(1)


