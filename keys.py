#from aztec_code_generator import AztecCode

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

import time
import base64
import random
import binascii
import qrcode

masterkeypem = b'-----BEGIN PRIVATE KEY-----\nMIG2AgEAMBAGByqGSM49AgEGBSuBBAAiBIGeMIGbAgEBBDDGokHL9IFveoU/i65P\nnzySq4xD8W3AyMwaLaDzvWMNIeD1Y4kI2w0mrJdZiybDWkGhZANiAAQL0+j9MKuY\nminc5M8saSfAxBeycBUZw/8PcqO+L33CeVDldefAc1drDkfc+ZUBcaSR4QeioQno\nuQXFqRayv4IpzhPwod/NE04CyWlCtee9XrZa7qSPlgWYM37QivJWml0=\n-----END PRIVATE KEY-----'
publicmasterkey = b'-----BEGIN PUBLIC KEY-----\nMHYwEAYHKoZIzj0CAQYFK4EEACIDYgAEC9Po/TCrmJop3OTPLGknwMQXsnAVGcP/\nD3Kjvi99wnlQ5XXnwHNXaw5H3PmVAXGkkeEHoqEJ6LkFxakWsr+CKc4T8KHfzRNO\nAslpQrXnvV62Wu6kj5YFmDN+0IryVppd\n-----END PUBLIC KEY-----\n'


def generate_private_key_pem():
    key = ec.generate_private_key(ec.SECP384R1).private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.PKCS8,encryption_algorithm=serialization.NoEncryption())
    return key

def generate_private_key():
    return ec.generate_private_key(ec.SECP384R1)

def private_key_to_pem(key):
    return key.private_bytes(encoding=serialization.Encoding.PEM,format=serialization.PrivateFormat.PKCS8,encryption_algorithm=serialization.NoEncryption())
    
def private_pem_to_key(pem):
    return serialization.load_pem_private_key(pem, password=None)

def public_key_to_pem(key):
    return key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

def public_pem_to_key(pem):
    return serialization.load_pem_public_key(pem)

def generate_shared_key(private, public):
    #bytetime = base64.b64encode(str(time.time()).encode())

    private_key = private
    public_key = public
    
    shared_key = private_key.exchange(ec.ECDH(), public_key)
    return shared_key

#derived_key = HKDF(algorithm=hashes.SHA256(),length=256, salt=None, info=None).derive(shared_key)

#bytetime = int(time.time()).to_bytes()

def derive_new_key_from_time(shared_key):
    
    bytetime = base64.b64encode(str(round(time.time(), -1)).encode())
    
    derived_key = HKDF(algorithm=hashes.SHA256(),length=256, salt=None, info=bytetime).derive(shared_key)
    return derived_key

def generate_aztec_from_key(key, name, path):
    #print(key)
    aztec = AztecCode(f"{name},{key}")
    aztec.save("az.png" , module_size=14, border=1)

def generate_qr_from_key(key):
    img = qrcode.make(f"{key}")
    
    return img
    
    

#publicmasterkey = private_pem_to_key(masterkeypem)

#publicmasterkey = publicmasterkey.public_key()

if __name__ == "__main__":
    shared_key = generate_shared_key(generate_private_key_pem(), generate_private_key_pem())
    while True:
         derived_key = derive_new_key_from_time(shared_key)
         generate_aztec_from_key(binascii.b2a_base64(derived_key))
         generate_qr_from_key("server", binascii.b2a_base64(derived_key))
         time.sleep(10)



# load PEM key

#x = serialization.load_pem_private_key(x, password=None)

# derive key

#derived_key = HKDF(algorithm=hashes.SHA256(),length=256, salt=None, info=None).derive(shared_key)