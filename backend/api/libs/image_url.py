from urllib.parse import urlencode
from flask import current_app
from .sign_url import encrypt_id, sign_url


class ImageURLBuilder(object):

    def __init__(self):
        self.aes_key = current_app.config.get('AES_KEY').encode('utf-8')
        self.aad = current_app.config.get('AAD').encode('utf-8')
        self.sign_key = current_app.config.get('SIGN_KEY').encode('utf-8')
        self.app_web_url = current_app.config.get("APP_WEB_URL")

    def build_image_url(self, prefix, image, expire):
        token = encrypt_id(self.aes_key, image.id, self.aad)
        path = f"{prefix}/{token}"

        signature = sign_url(self.sign_key, path, expire)
        query = urlencode({'expires': expire, 'sig': signature})

        image_url = f'{self.app_web_url}{path}?{query}'

        path = f"{prefix}/{token}/300x200"
        signature = sign_url(self.sign_key, path, expire)
        query = urlencode({'expires': expire, 'sig': signature})
        thumbnail_url = f'{self.app_web_url}{path}?{query}'

        return {
            'image_url': image_url,
            'thumbnail_url': thumbnail_url,
        }
