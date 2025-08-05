#!/usr/bin/env python
"""
Celery Beat 调度器启动脚本
包含信号处理和优雅关闭机制
"""

import os
import sys
import signal
import logging
from celery import Celery
from api.api_app import create_app

# 设置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = create_app()

# 获取Celery实例
celery_app = app.extensions["celery"]

# 全局变量用于跟踪关闭状态
_shutdown_requested = False


def signal_handler(signum, frame):
    """信号处理器"""
    global _shutdown_requested
    logger.info(f"收到信号 {signum}，开始优雅关闭Celery beat...")
    _shutdown_requested = True

    # 发送关闭信号给Celery beat
    try:
        celery_app.control.shutdown()
        logger.info("已发送关闭信号给Celery beat")
    except Exception as e:
        logger.error(f"发送关闭信号失败: {e}")

    # 退出进程
    sys.exit(0)


def main():
    """主函数"""
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # kill

    logger.info("启动Celery beat调度器...")

    try:
        # 启动Celery beat
        celery_app.worker_main(
            ["beat", "--loglevel=info", "--scheduler=celery.beat:PersistentScheduler"]
        )
    except KeyboardInterrupt:
        logger.info("收到键盘中断，正在关闭...")
    except Exception as e:
        logger.error(f"Celery beat启动失败: {e}")
        sys.exit(1)
    finally:
        logger.info("Celery beat已关闭")


if __name__ == "__main__":
    main()
