import base64
import hashlib
import os

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


# Generate a random salt for the password-based key
def generate_salt():
    return os.urandom(16)


# Derive an encryption key from the master password
def derive_key(master_password, salt):
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1
    )

    key = kdf.derive(master_password.encode("utf-8"))

    return base64.urlsafe_b64encode(key)


# Encrypt data
def encrypt_data(data, master_password, salt):
    key = derive_key(master_password, salt)

    cipher = Fernet(key)

    encrypted_data = cipher.encrypt(data.encode("utf-8"))

    return encrypted_data


# Decrypt data
def decrypt_data(encrypted_data, master_password, salt):
    key = derive_key(master_password, salt)

    cipher = Fernet(key)

    try:
        decrypted_data = cipher.decrypt(encrypted_data)

        return decrypted_data.decode("utf-8")

    except InvalidToken:
        raise ValueError("Incorrect master password or corrupted vault.")