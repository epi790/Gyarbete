import sqlite
import keys

cursor = sqlite.init()

query = "select key from users;"

cursor.execute(query)

result = cursor.fetchall()

#print(result[0])

new_key = []
key_pem = []

for i in result:
    
    key_pem.append(keys.private_pem_to_key(i))

for i in key_pem:
    new_key.append(keys.derive_new_key_from_time(i))
    


print(new_key)