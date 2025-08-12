import logging
import base64
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from api.extensions.storage import storage


class EncryptStruct(object):
    prefix = "aiflow:v1:"

    def __init__(self, prefix="") -> None:
        if prefix:
            self.prefix = prefix

    def pack(self, encrypted_aes_key, nonce, digest, ciphertext):
        return self.prefix + encrypted_aes_key + nonce + digest + ciphertext

    def unpack(self, encrypted_data):
        if not encrypted_data.startswith(self.prefix):
            raise ValueError("Invalid encrypted data")

        prefix_length = len(self.prefix)
        encrypted_aes_key = encrypted_data[prefix_length : prefix_length + 16]
        nonce = encrypted_data[prefix_length + 16 : prefix_length + 32]
        digest = encrypted_data[prefix_length + 32 : prefix_length + 48]
        ciphertext = encrypted_data[prefix_length + 48 :]

        return encrypted_aes_key, nonce, digest, ciphertext


def get_user_private_filepath(user_id):
    return f"privkeys/{user_id}/private.pem"


def generate_key_pair(user_id, key_size=2048):
    key = RSA.generate(key_size)

    private_key = key.export_key()
    filepath = get_user_private_filepath(user_id)
    storage.save(filepath, private_key)

    public_key = key.publickey().export_key()
    return public_key.decode()


def encrypt(text, public_key, prefix):
    aes_key = get_random_bytes(16)

    rsa_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)

    cipher_aes = AES.new(aes_key, AES.MODE_EAX)
    ciphertext, digest = cipher_aes.encrypt_and_digest(text.encode())

    struct = EncryptStruct(prefix)
    return struct.pack(encrypted_aes_key, cipher_aes.nonce, digest, ciphertext)


def decrypt(user_id, encrypted_data, prefix):
    filepath = get_user_private_filepath(user_id)
    private_key = storage.load(filepath)
    rsa_key = RSA.import_key(private_key)  # type: ignore
    cipher_rsa = PKCS1_OAEP.new(rsa_key)

    struct = EncryptStruct(prefix)
    encrypted_aes_key, nonce, digest, ciphertext = struct.unpack(encrypted_data)

    aes_key = cipher_rsa.decrypt(encrypted_aes_key)
    cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)

    decrypted_text = cipher_aes.decrypt_and_verify(ciphertext, digest)

    return decrypted_text
