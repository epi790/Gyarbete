import keys
import pickle
import os
import time
from PIL import Image

# init, load keys

shared_key = ""

if os.path.isfile("client_private_key_pickle.pk"):
    pass
else:
    file = open("client_private_key_pickle.pk", "a")
    file.close()


with open("client_private_key_pickle.pk", 'rb') as fi:
    try:
        private_key = pickle.load(fi)
        private_key = keys.private_pem_to_key(private_key)
        
        shared_key = pickle.load(fi)
        print(f"LOADING SHARED KEY")
        
    except:
        private_key = None
        pass

    if private_key != None:
        print("PRIVATE KEY FOUND")
        #print("SHARED KEY:", shared_key)
    else:
        print("OVERRIDING KEY")
        private_key = keys.generate_private_key()
        
    
if shared_key == "":
    shared_key = keys.generate_shared_key(private_key, keys.public_pem_to_key(keys.publicmasterkey))
    with open("client_private_key_pickle.pk", 'wb') as fi:
        print("OPENING FILE")
        pickle.dump(keys.private_key_to_pem(private_key), fi)

        if shared_key != "":
            pickle.dump(shared_key, fi)


#shared key loaded guarantee

print(shared_key)

keys.generate_qr_from_key(keys.public_key_to_pem(private_key.public_key())).save("clientpubkey.png")
while True:
    derived = keys.derive_new_key_from_time(shared_key)
    qr = keys.generate_qr_from_key(derived)

    qr.save("client_derived_key.png")
    
    time.sleep(10)





    