from api.extensions.redis import redis_client
from api.libs.helper import generate_captcha_code
from api.libs.exceptions import CaptchaError


class CaptchaService(object):

    captcha_prefix = "captcha:"

    @staticmethod
    def get_key(mobile):
        return CaptchaService.captcha_prefix + mobile

    @staticmethod
    def send_captcha_code(mobile):
        key = CaptchaService.get_key(mobile)
        code = generate_captcha_code(4)
        redis_client.set(key, code)

    @staticmethod
    def valid_captcha_code(mobile, code):
        key = CaptchaService.get_key(mobile)
        value = redis_client.get(key)
        if value is None:
            raise CaptchaError("expiration captcha")

        if value == code:
            return value
        else:
            raise CaptchaError("captcha invalid")
