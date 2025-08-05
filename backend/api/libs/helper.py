import datetime
from hashlib import sha256, sha1
import uuid
import re
import string
import random
import ulid
from functools import partial

from flask_restful import fields


def app_token():
    v = str(uuid.uuid4())
    fields = v.split("-")
    token = ulid.ulid() + fields[0]
    return token


def validate_email(email):
    pattern = r"^[\w\.-]+@([\w-]+\.)+[\w-]{2,}$"
    if re.match(pattern, email) is not None:
        return email

    error = f"{email} is not a valid email."
    raise ValueError(error)


def get_remote_ip(request):
    if request.headers.get("CF-Connecting-IP"):
        return request.headers.get("CF-Connecting-IP")
    elif request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For")
    else:
        return request.remote_addr


def text_sha256(text):
    return sha256(text).hexdigest()


def random_string(n):
    source = string.ascii_letters + string.digits
    return "".join((random.choice(source) for i in range(n)))


def is_valid_authorization(auth_header):
    return auth_header.startswith("Bearer ")


def merge_dict(origin, merged):
    return {}


class TimestampField(fields.Raw):
    def format(self, value) -> str:
        return str(int(value.timestamp()) * 1000 + int(value.microsecond / 1000))


def timestamp_to_datetime_with_ms(timestamp_ms):
    seconds, ms = divmod(timestamp_ms, 1000)

    dt = datetime.datetime.fromtimestamp(seconds)
    dt = dt + datetime.timedelta(milliseconds=ms)
    return dt


def generate_captcha_code(length=4):
    return "".join(random.choices(string.digits, k=length))


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def generate_string(n):
    letters_digits = string.ascii_letters + string.digits
    result = ""
    for i in range(n):
        result += random.choice(letters_digits)

    return result


def generate_text_hash(text: str) -> str:
    hash_text = str(text) + "None"
    return sha256(hash_text.encode()).hexdigest()


def digest(buff):
    return sha1(buff).hexdigest()


def digest_file(file_path):
    with open(file_path, "rb") as f:
        return digest(f.read())


generate_invited_code = partial(random_string, 6)
