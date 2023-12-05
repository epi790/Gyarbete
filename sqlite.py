import sqlite3
import keys
import time

def init():
    database = sqlite3.connect("rudbeck.db")
    cursor = database.cursor()

    return cursor


def get_name_from_key(key_pem):
    query = f"select name from users where key is {key_pem}"
    cursor.execute(query)
    result = cursor.fetchall()

    return result

#query = "select key from users;"

#cursor.execute(query)

#result = cursor.fetchall()


#print(result[0])


# for i in result:
#     print(i)
    
#     #print(keys.derive_new_key_from_time())