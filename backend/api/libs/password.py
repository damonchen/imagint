import re
import hashlib
import secrets

password_pattern = r"^(?=.*[a-zA-Z])(?=.*\d).{8,}$"


def validate_password(password):
    if re.match(password_pattern, password) is not None:
        return password

    raise ValueError("Not a valid password")


def generate_password_salt(size=16):
    salt = secrets.token_bytes(size)
    return salt.hex()


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 10000).hex()


def compare_password(password, hashed_password, salt):
    salt = bytes.fromhex(salt)
    return hash_password(password, salt) == hashed_password


def generate_password_reset_token():
    return generate_password_salt(size=32)
