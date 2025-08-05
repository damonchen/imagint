from libs.opaque import OpaqueEncoder


class OpaqueEncoderProxy(object):

    def __init__(self, app=None):
        self.init_app(app)

    def init_app(self, app=None):
        if app is not None:
            self.app = app
            secret_key = app.config.get('OPAQUE_SECRET_KEY')
            self.opaque = OpaqueEncoder(secret_key)

    def encode(self, i):
        return self.opaque.encode_base64(i)

    def decode(self, i):
        return self.opaque.decode_base64(i)


opaque = OpaqueEncoderProxy()


def init_app(app=None):
    opaque.init_app(app)
