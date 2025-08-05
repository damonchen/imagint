#!/usr/bin/env python
"""
Celery Worker 启动脚本
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
    logger.info(f"收到信号 {signum}，开始优雅关闭Celery worker...")
    _shutdown_requested = True

    # 发送关闭信号给Celery worker
    try:
        celery_app.control.shutdown()
        logger.info("已发送关闭信号给Celery worker")
    except Exception as e:
        logger.error(f"发送关闭信号失败: {e}")

    # 退出进程
    sys.exit(0)


def main():
    """主函数"""
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # kill

    logger.info("启动Celery worker...")

    try:
        # 启动Celery worker
        celery_app.worker_main(
            [
                "worker",
                "--loglevel=info",
                "--concurrency=4",  # 可以根据需要调整并发数
                "--without-gossip",
                "--without-mingle",
                "--without-heartbeat",
            ]
        )
    except KeyboardInterrupt:
        logger.info("收到键盘中断，正在关闭...")
    except Exception as e:
        logger.error(f"Celery worker启动失败: {e}")
        sys.exit(1)
    finally:
        logger.info("Celery worker已关闭")


if __name__ == "__main__":
    main()
