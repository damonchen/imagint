#!/usr/bin/env python
"""
测试信号处理和优雅关闭功能
"""

import os
import sys
import signal
import time
import logging
from api.api_app import create_app

# 设置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_signal_handling():
    """测试信号处理"""
    logger.info("开始测试信号处理...")

    # 创建应用
    app = create_app()

    def signal_handler(signum, frame):
        logger.info(f"测试：收到信号 {signum}")
        app.shutdown()
        sys.exit(0)

    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.info("应用已启动，按Ctrl+C测试关闭功能...")
    logger.info("或者等待10秒后自动退出...")

    try:
        # 模拟应用运行
        for i in range(10):
            logger.info(f"应用运行中... {i+1}/10")
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("收到键盘中断")
    except Exception as e:
        logger.error(f"测试过程中出错: {e}")
    finally:
        logger.info("测试完成")


def test_celery_extension():
    """测试Celery扩展"""
    logger.info("测试Celery扩展...")

    try:
        app = create_app()

        # 检查Celery扩展是否正确初始化
        if "celery" in app.extensions:
            celery_app = app.extensions["celery"]
            logger.info("Celery扩展初始化成功")

            # 测试关闭方法
            if hasattr(celery_app, "shutdown"):
                logger.info("Celery扩展支持shutdown方法")
            else:
                logger.warning("Celery扩展不支持shutdown方法")

        else:
            logger.error("Celery扩展未找到")

    except Exception as e:
        logger.error(f"测试Celery扩展时出错: {e}")


if __name__ == "__main__":
    logger.info("=== 信号处理和优雅关闭测试 ===")

    # 测试Celery扩展
    test_celery_extension()

    print("\n" + "=" * 50)
    print("按Enter键开始信号处理测试...")
    input()

    # 测试信号处理
    test_signal_handling()
