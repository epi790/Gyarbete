import keys
from keys import masterkeypem
import qrreader
import sqlite3
import time

print(masterkeypem)

database = sqlite3.connect("rudbeck.db")
cursor = database.cursor()


def get_name_from_key(key_pem):
    query = f'select name from users where key is "{key_pem}";'
    
    cursor.execute(query)
    result = cursor.fetchall()

    return result

def give_access():
    return 1


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
        dbname = get_name_from_key(key_pem)

        if dbname == name:
            give_access()
            
    print(result) 
    time.sleep(1)


