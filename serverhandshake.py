import keys
from masterkey import masterkey
import qrreader
import sqlite3
import time
import base64

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
    shared_key = base64.b64encode(shared_key)
    print("CALlEd")
    print(f"{name},{shared_key})")
    query = f'insert or ignore into shared VALUES("{name}", "{shared_key}")'
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
        #result = base64.b64decode(result)
        key_pem, name = result.split(",")
        print("CAllING...")
        print(keys.public_pem_to_key(key_pem.encode()))

        sharedkey = keys.generate_shared_key(keys.private_pem_to_key(masterkey), keys.public_pem_to_key(key_pem.encode()))
        print(sharedkey)
      
        adduser(name, sharedkey)
        exit()

  
    time.sleep(1)


