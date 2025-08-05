#!/usr/bin/env python
"""
快速启动脚本
用于开发和测试环境
"""

import os
import sys
import signal
import logging
import subprocess
import time
from api.api_app import create_app

# 设置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def check_dependencies():
    """检查依赖服务"""
    logger.info("检查依赖服务...")

    # 检查Redis
    try:
        import redis

        r = redis.Redis(host="localhost", port=6379, db=0)
        r.ping()
        logger.info("✓ Redis服务正常")
    except Exception as e:
        logger.warning(f"✗ Redis服务异常: {e}")

    # 检查RabbitMQ
    try:
        import pika

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost", port=5672)
        )
        connection.close()
        logger.info("✓ RabbitMQ服务正常")
    except Exception as e:
        logger.warning(f"✗ RabbitMQ服务异常: {e}")

    # 检查PostgreSQL
    try:
        from sqlalchemy import create_engine

        engine = create_engine("postgresql://imgint:password@localhost:5434/imgint")
        engine.connect().close()
        logger.info("✓ PostgreSQL服务正常")
    except Exception as e:
        logger.warning(f"✗ PostgreSQL服务异常: {e}")


def start_flask_only():
    """仅启动Flask应用"""
    logger.info("启动Flask应用...")

    app = create_app()

    def signal_handler(signum, frame):
        logger.info(f"收到信号 {signum}，关闭Flask应用...")
        app.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        app.run(host="0.0.0.0", port=5080, debug=True)
    except KeyboardInterrupt:
        logger.info("收到键盘中断")
    except Exception as e:
        logger.error(f"Flask应用启动失败: {e}")


def start_with_celery():
    """启动Flask应用和Celery"""
    logger.info("启动Flask应用和Celery...")

    # 启动Celery worker
    worker_process = subprocess.Popen(
        [sys.executable, "celery_worker.py"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
    )

    time.sleep(2)  # 等待worker启动

    # 启动Flask应用
    app = create_app()

    def signal_handler(signum, frame):
        logger.info(f"收到信号 {signum}，关闭所有服务...")

        # 关闭Celery worker
        if worker_process.poll() is None:
            worker_process.terminate()
            worker_process.wait(timeout=5)

        app.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        app.run(host="0.0.0.0", port=5080, debug=True)
    except KeyboardInterrupt:
        logger.info("收到键盘中断")
    finally:
        if worker_process.poll() is None:
            worker_process.terminate()


def main():
    """主函数"""
    print("=== Flask + Celery 快速启动 ===")
    print("1. 检查依赖服务")
    print("2. 仅启动Flask应用")
    print("3. 启动Flask应用 + Celery")
    print("4. 启动所有服务（Flask + Celery + Beat）")
    print("5. 测试信号处理")
    print("0. 退出")

    while True:
        try:
            choice = input("\n请选择 (0-5): ").strip()

            if choice == "0":
                print("退出...")
                break
            elif choice == "1":
                check_dependencies()
            elif choice == "2":
                start_flask_only()
            elif choice == "3":
                start_with_celery()
            elif choice == "4":
                print("启动所有服务...")
                subprocess.run([sys.executable, "start_services.py"])
            elif choice == "5":
                print("运行信号处理测试...")
                subprocess.run([sys.executable, "test_shutdown.py"])
            else:
                print("无效选择，请重新输入")

        except KeyboardInterrupt:
            print("\n退出...")
            break
        except Exception as e:
            logger.error(f"出错: {e}")


if __name__ == "__main__":
    main()
