import keys
from masterkey import masterkey
import qrreader
import sqlite3
import time
import base64
import ast
import arduino

#print(masterkey)

database = sqlite3.connect("rudbeck.db")
cursor = database.cursor()


def get_key_from_name(name):

    query = f'select sharedkey from shared where name is "{name}";'
    
    cursor.execute(query)
    result = cursor.fetchone()

    if result is None:
        return False

    result = base64.b64decode(ast.literal_eval(result[0]))
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
    #result = "b'\x7f\x1d\x9aAR \xd6\x93\x90\x0f9\xea\xec\xba\xe6UC\\\x87p\x10\x0f?\xe6z\x17\xa3{uEs\xd0z\x8a\x8c\xc9\xd1O\xa8O\xf6\x11\xcc\x07\xc50\x98\x1c\xe1\x83q}\xce\xa6\xde9e\x95\x94e\x804(\xea', Alve"
    if result == None:
        #pass
        continue

    
    #print(base64.b64decode(result))

    #result = base64.b64decode(result.decode()).decode()
    result = ast.literal_eval(result)

    result = base64.b64decode(result.decode()).decode()

    #print(result)
    
    #################### VIKTIGT #####################
    key_pem, name = result.split(", ")
    name = name.replace(' ', '')
    ############ test utan telefon ############# 

    # key_pem = """b')T\xb6vC\xb7\xf8\x9d\xf6\xb1[/\xd2\xf6X\x86\x109\xf4\xc8y;\xc6e\xed\xf5\xdc\xd6\x0b\xea\xb1\x9cu\xed\xc2\x9aB5\xb2\xe5\x12\x82\xe7I\xc0\xd6\xb1T\x93\xc8\x13\xf8"\x85\xad\xf2%X\x02NF\x1b\x95\xbe'"""
    # name = "Alve"
    #key_pem += "'"

    #print(key_pem, name)

    if key_pem and name is not None:
        if get_key_from_name(name):
            sharedkey = get_key_from_name(name)
        else:
            print("User not in databse")
            time.sleep(1)
            continue

        #print(sharedkey)
        if sharedkey == None:
            time.sleep(1)
            continue
        #print("\n"*3)
        
        #print(sharedkey)
        key_now = keys.derive_new_key_from_time(sharedkey)

        def transform(key):
            #key = bytes(key)
            #print(key)
            #print(type(key))
            return key
        
        key_now = transform(key_now)
        key_pem = transform(ast.literal_eval(key_pem))

        print(f"Key now: {key_now}")
        print(f"key pem: {key_pem}")
        #print( ast.literal_eval(key_now.hex()) == ast.literal_eval(key_pem).hex())
        print(key_now == key_pem)

        if key_now == key_pem: 
            give_access()
            #arduino.send_light("G")
        else:
            #arduino.send_light("R")
            print("NUH UH ")

            
    #print(result) 
    


