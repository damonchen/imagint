import base64
import time
import os
import hashlib
import hmac
import logging
from typing import Optional

from flask import current_app
from flask.cli import F

from ...extensions.storage import storage

logger = logging.getLogger("core.file.attachment_image_parser")


class AttachmentImageParser(object):

    @staticmethod
    def get_image_data(attachment, force_url=False) -> Optional[str]:
        if not attachment:
            return None

        if not attachment.is_image:
            return None

        if current_app.config["SEND_IMAGE_FORMAT"] == "url" or force_url:
            return AttachmentImageParser.get_signed_temp_image_url(attachment.id)

        try:
            data = storage.load(attachment.key)
        except FileNotFoundError:
            logger.error(f"File not found: {attachment.key}")
            return None

        encoded = base64.b64encode(data).decode("utf-8")

        return f"data:{attachment.mime_type};base64,{encoded}"

    @staticmethod
    def get_signed_temp_image_url(attachment_id) -> str:
        base_url = current_app.config.get("FILEs_URL")
        image_preview_url = f"{base_url}/files/{attachment_id}/preview"

        timestamp = str(int(time.time()))
        nonce = os.urandom(16).hex()
        data = f"image-preview:{attachment_id}:{timestamp}:{nonce}"
        secret_key = current_app.config["SECRET_KEY"].encode()
        signed = hmac.new(secret_key, data.encode(), hashlib.sha256).hexdigest()

        return (
            f"{image_preview_url}?timestamp={timestamp}&nonce={nonce}&signed={signed}"
        )

    @staticmethod
    def verify_image_preview(attachment_id, timestamp, nonce, signed) -> bool:
        secret_key = current_app.config["SECRET_KEY"].encode()
        data = f"image-preview:{attachment_id}:{timestamp}:{nonce}"
        if not hmac.compare_digest(
            signed, hmac.new(secret_key, data.encode(), hashlib.sha256).hexdigest()
        ):
            return False

        current_time = int(time.time())
        return current_time - int(timestamp) <= 5 * 60  # 5 minutes
