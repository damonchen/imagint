from flask import (
    Blueprint,
    current_app,
    make_response,
    request,
    g,
    Response,
)
from werkzeug.utils import secure_filename
from pypinyin import lazy_pinyin

from api.utils.decorator import api_json
from api.libs.decorator import token_required, any_required
from api.extensions.database import db
from api.extensions.storage import storage
from api.services.attachment_service import AttachementService

bp = Blueprint("attachment", __name__)


def allowed_file_extensions(filename):
    allowed_iamge_extensions = current_app.config.get("ALLOWED_IMAGE_EXTENSIONS")
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in allowed_iamge_extensions
    )


# @api_json()
@bp.route("/attachment/upload", methods=["POST"])
@token_required
@api_json()
def upload_attachment():
    if "file" not in request.files:
        return {"status": "error", "message": "No file part"}

    file = request.files["file"]
    if not file.filename:
        return {"status": "error", "message": "No selected file"}

    print("file.filename", file.filename)
    # pinyin for 汉字问题
    filename = secure_filename("".join(lazy_pinyin(file.filename)))
    if not allowed_file_extensions(filename):
        return {"status": "error", "message": "File type not allowed"}

    file_size_limit = (
        current_app.config.get("UPLOAD_IMAGE_FILE_SIZE_LIMIT", 10) * 1024 * 1024
    )

    file_size = file.content_length
    if file_size > file_size_limit:
        return {"status": "error", "message": "File size too large"}

    content_type = file.content_type
    container_id = request.form.get("container_id")
    container_type = request.form.get("container_type")
    if not container_id or not container_type:
        return {"status": "error", "message": "container_id or container_type is empty"}

    account = g.account
    attachemnt = AttachementService.save_attachment(
        container_id, container_type, filename, file.read(), content_type, account.id
    )

    return {
        "attachment": attachemnt.id,
    }


@bp.route("/attachment/<int:pk>", methods=["GET"])
@any_required([token_required])
def attachment(pk):
    attachment = AttachementService.load_attachment(pk)
    if not attachment:
        return make_response("Not found", 404)

    response = Response(attachment.content, mimetype=attachment.content_type)
    return response
