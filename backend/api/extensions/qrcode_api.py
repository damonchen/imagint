# # 通过调用外部的api service来构建具体的二维码
# import requests


# class WebApi(object):
#     headers = {
#         'User-Agent': "web app v1.0.0"
#     }

#     def __init__(self, app=None):
#         if app is not None:
#             self.init_app(app)

#     def init_app(self, app=None):
#         self.app = app
#         if app is not None:
#             self.api_url = app.config.get('QRCODE_API_URL')
#             self.api_key = app.config.get('QRCODE_API_KEY')

#     def create_qrcode(self, content, style):
#         """
#         Create a new QR code
#         Args:
#             data: Data to encode in QR code
#         Returns:
#             Generated QR code image
#         """
#         try:
#             api_url = f'{self.api_url}/api/qrcode'
#             data = {
#                 'content': content,
#                 'style': style,
#             }
#             headers = self.headers.copy()
#             headers['Authentication'] = f'Bearer {self.api_key}'
#             resp = requests.post(api_url, headers=headers, data=data)
#             return resp.json()
#         except Exception as e:
#             raise Exception(f"Error creating QR code: {str(e)}")


# qrcode_api = WebApi()

# def init_app(app=None):
#     qrcode_api.init_app(app)
