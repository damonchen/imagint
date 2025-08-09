import os
from flask import request, abort, current_app, send_file
from flask_restful import Resource, reqparse

from api.services.chat_service import ChatMessageImageService
from api.libs.sign_url import verify_signature, decrypt_token
from api.service.redis_service import RedisService
from . import api


class BaseFileResource(Resource):

    def _get(self, file_token):
        parser = reqparse.RequestParser()
        parser.add_argument("expires", type=int, location="args")
        parser.add_argument("sig", type=str, location="args")
        args = parser.parse_args()

        sig = args.sig
        expires = args.expires
        path = request.path

        if not expires or not sig or not verify_signature(path, expires, sig):
            abort(403, "Signature invalid or expired")

        # 检查一次性 token 是否已经使用
        if RedisService.get(f"used:{file_token}"):
            abort(403, "URL already used")
        RedisService.set(f"used:{file_token}", 1, 3600)  # 防重用，1小时保留记录

        aes_key = current_app.config.get("AES_KEY")

        try:
            aad = b"file-service"
            file_id = decrypt_token(aes_key, file_token, aad)
        except ValueError:
            abort(400, "Invalid file token")

        return file_id


class ImageResource(BaseFileResource):

    def get(self, file_token):
        file_id = self._get(file_token)
        image = ChatMessageImageService.get_image(image_id=file_id)
        if not image or not os.path.exists(image):
            abort(404, "File not found")

        # 得到image对象，然后通过send的方式发送文件出去
        return send_file(image.image_path, as_attachment=True)


# 可能也得有一个文件上传的token限制处理，防止恶意上传
class FileUploadResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("file", type=FileStorage, location="files")
        parser.add_argument("media_type", type=str, location="args")
        args = parser.parse_args()
        file = args.file
        media_type = args.media_type

        if not file:
            abort(400, "No file uploaded")

        file_id = str(uuid.uuid4())
        if media_type == "image":
            image_path = os.path.join(
                current_app.config.get("IMAGE_PATH"), file_id[:2], f"{file_id}.png"
            )
            file.save(image_path)
        elif media_type == "video":
            video_path = os.path.join(
                current_app.config.get("VIDEO_PATH"), file_id[:2], f"{file_id}.mp4"
            )
            file.save(video_path)

        return {"file_id": file_id}


api.add_resource(ImageResource, "/image/<file_token>")

api.add_resource(FileUploadResource, "/file/upload")
