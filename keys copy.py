
from aztec_code_generator import AztecCode

from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.asymmetric import ec

from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.kdf.hkdf import HKDF

import time
import base64
import random
import binascii




def generate_shared_key():
    # Get tiem and round to 10th second as info for the key derivation
    bytetime = base64.b64encode(str(time.time()).encode())
    #generate key from predefined eliptic curve
    server_private_key = ec.generate_private_key(ec.SECP384R1)
    #print(server_private_key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo))
    
    client_private_key = ec.generate_private_key(ec.SECP384R1)
    
    shared_key = server_private_key.exchange(ec.ECDH(), client_private_key.public_key())

    return shared_key

#derived_key = HKDF(algorithm=hashes.SHA256(),length=256, salt=None, info=None).derive(shared_key)

#bytetime = int(time.time()).to_bytes()

def derive_new_key_from_time(shared_key):
    bytetime = base64.b64encode(str(round(time.time(), -1)).encode())
    derived_key = HKDF(algorithm=hashes.SHA256(),length=256, salt=None, info=bytetime).derive(shared_key)
    return derived_key

def generate_aztec_from_key(key):
    print(key)
    aztec = AztecCode(key)
    aztec.save("az.png" , module_size=16, border=1)

if __name__ == "__main__":
    shared_key = generate_shared_key()
    while True:
         derived_key = derive_new_key_from_time(shared_key)
         generate_aztec_from_key(binascii.b2a_base64(derived_key))
         time.sleep(10)



# print(derived_key)

# aztec = AztecCode(derived_key)

# aztec.save('/www/gyar/az.png', module_size=16, border=1)


#derived_key.decode('hex')