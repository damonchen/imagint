import hashlib
import secrets
import hmac
import time

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# base36 编码表
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"


def int_to_base36(n: int) -> str:
    if n == 0:
        return "0"
    s = []
    base = 36
    while n:
        n, r = divmod(n, base)
        s.append(ALPHABET[r])
    return "".join(reversed(s))


def base36_to_int(s: str) -> int:
    base = 36
    n = 0
    for ch in s:
        n = n * base + ALPHABET.index(ch)
    return n


# ==============================
# AES-GCM 加解密
# ==============================
VERSION_BYTE = b"\x01"


def encrypt_id(aes_key: bytes, internal_id: int, aad: bytes = None, nonce_size: int = 12) -> str:
    aesgcm = AESGCM(aes_key)
    nonce = secrets.token_bytes(nonce_size)
    id_bytes = internal_id.to_bytes((internal_id.bit_length() + 7) // 8 or 1, "big")
    ct = aesgcm.encrypt(nonce, id_bytes, aad)
    payload = VERSION_BYTE + nonce + ct
    as_int = int.from_bytes(payload, "big")
    return int_to_base36(as_int)


def decrypt_token(aes_key: bytes, token: str, aad: bytes = None, nonce_size: int = 12) -> int:
    try:
        as_int = base36_to_int(token)
        payload = as_int.to_bytes((as_int.bit_length() + 7) // 8 or 1, "big")
        if len(payload) < 1 + nonce_size + 16 + 1:
            raise ValueError("payload too short")
        ver = payload[0:1]
        if ver != VERSION_BYTE:
            raise ValueError("unsupported token version")
        nonce = payload[1:1 + nonce_size]
        ct = payload[1 + nonce_size:]
        aesgcm = AESGCM(aes_key)
        id_bytes = aesgcm.decrypt(nonce, ct, aad)
        internal_id = int.from_bytes(id_bytes, "big")
        return internal_id
    except Exception:
        raise ValueError("invalid token")


# ==============================
# 签名工具
# ==============================
def sign_url(sign_key: bytes, path: str, expires: int) -> str:
    """
    给 path + expires 做 HMAC-SHA256 签名
    """
    msg = f"{path}?expires={expires}".encode()
    sig = hmac.new(sign_key, msg, hashlib.sha256).hexdigest()
    return sig


def verify_signature(sign_key: bytes, path: str, expires: int, sig: str) -> bool:
    if time.time() > expires:
        return False
    expected = sign_url(sign_key, path, expires)
    return hmac.compare_digest(expected, sig)
