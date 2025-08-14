# tasks.py
import logging
import os
import time
from datetime import datetime, timedelta
from flask import current_app
from apscheduler.schedulers.background import BackgroundScheduler
from api.services.attachment_service import AttachementService
from api.services.repository.attachment_repository import AttachmentRepository
from api.extensions.database import transaction


def _cleanup_files():
    """定时清理任务"""
    # 清理待删除文件
    attachements = AttachementService.load_attachments_by_status("to_delete")
    for attachement in attachements:
        try:
            if os.path.exists(attachement.storage_path):
                os.remove(attachement.storage_path)
            AttachmentRepository.delete_attachment(attachement)
        except Exception as e:
            current_app.logger.error(f"Delete failed: {attachement.id} - {str(e)}")

    # 清理过期临时文件（超过24小时未处理）
    expiry_time = time.time() - current_app.config["TEMP_FILE_EXPIRY"]
    expired_attachements = AttachementService.load_attachments_by_status(
        "temp", expiry_time
    )

    for attachement in expired_attachements:
        try:
            if os.path.exists(attachement.storage_path):
                os.remove(attachement.storage_path)
            AttachmentRepository.delete_attachment(attachement)
        except Exception as e:
            current_app.logger.error(f"Cleanup failed: {attachement.id} - {str(e)}")


@transaction
def cleanup_files():
    with current_app.app_context():
        """清理文件"""
        _cleanup_files()
        current_app.logger.info("Cleanup files task completed.")


# 启动定时任务（每小时运行一次）
scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_files, "interval", hours=1)
# scheduler.start()
