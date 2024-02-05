from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from time import time
from base64 import b64encode
from os import urandom

import binascii
import qrcode

publicmasterkey = b'-----BEGIN PUBLIC KEY-----\nMHYwEAYHKoZIzj0CAQYFK4EEACIDYgAEC9Po/TCrmJop3OTPLGknwMQXsnAVGcP/\nD3Kjvi99wnlQ5XXnwHNXaw5H3PmVAXGkkeEHoqEJ6LkFxakWsr+CKc4T8KHfzRNO\nAslpQrXnvV62Wu6kj5YFmDN+0IryVppd\n-----END PUBLIC KEY-----\n'


def generate_private_key_pem():
    key = ec.generate_private_key(ec.SECP384R1).private_bytes(encoding=serialization.Encoding.PEM,
                                                              format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
    return key


def generate_private_key():
    return ec.generate_private_key(ec.SECP384R1, backend=crypto_default_backend())


def private_key_to_pem(key):
    return key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption(), backend=crypto_default_backend())


def private_pem_to_key(pem):
    return serialization.load_pem_private_key(pem, password=None, backend=crypto_default_backend())


def public_key_to_pem(key):
    return key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)


def public_pem_to_key(pem):

    public_key = serialization.load_pem_public_key(
        pem, backend=crypto_default_backend())
    return public_key

    if hasattr(serialization, 'load_pem_public_key'):
        pass
    else:

        from cryptography.hazmat.primitives.asymmetric import dsa, rsa

        cert = serialization.load_pem_x509_certificate(
            pem, backend=crypto_default_backend())
        public_key = cert.public_key()

        if isinstance(public_key, (rsa.RSAPublicKey, dsa.DSAPublicKey)):
            return public_key


def generate_shared_key(private, public):
    private_key = private
    public_key = public
    shared_key = private_key.exchange(ec.ECDH(), public_key)
    return shared_key


def derive_new_key_from_time(shared_key):
    bytetime = b64encode(str(round(time(), -1)).encode())
    derived_key = HKDF(algorithm=hashes.SHA256(), length=64,
                       salt=None, info=bytetime).derive(shared_key)
    return derived_key


def generate_aztec_from_key(key, name, path):
    aztec = AztecCode(f"{name},{key}")
    aztec.save("az.png", module_size=14, border=1)


def generate_qr_from_key(key):
    img = qrcode.make(f"{key}")

    return img


def encrypt_AES256(message, key):
    iv = urandom(16)
    cipher = Cipher(algorithms.AES256(key), modes.CFB(iv),
                    backend=crypto_default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message) + encryptor.finalize()
    return ciphertext


def decrypt_AES256(message, key):

    cipher = Cipher(algorithms.AES256(key), backend=crypto_default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(message)
