import sqlite3
import keys
import sys
import random
import binascii
from cryptography.hazmat.primitives import serialization

database = sqlite3.connect("rudbeck.db")

cursor = database.cursor()

class User:
    def __init__(self, userid, name, key):
        self.userid = userid
        self.name = name
        self.key = key
    
def Adduser(User):
    query = f"insert into users values({User.userid}, \"{User.name}\", \"{User.key}\");"
    cursor.execute(query)


def share_key(name):
    query = f"select key from users where name is '{name}';"
    cursor.execute()


u = User(0, "", "")

u.userid = int(input("UID: "))
u.name = input("name: ")
u.key = input("Key: ")

Adduser(u)


#print(sys.argv[1])




#f = open("names", "r").read().splitlines()




#privatekey = keys.generate_private_key()


#print(query)

# for i in f:
#     x = User(0, i, keys.generate_private_key().private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()))
#     Adduser(x)


database.commit()


#result = cursor.fetchall()



#print(result)