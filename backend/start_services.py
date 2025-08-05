#!/usr/bin/env python
"""
服务启动脚本
管理Flask应用、Celery worker和beat的启动和关闭
"""

import os
import sys
import signal
import logging
import subprocess
import time
import threading
from typing import List, Optional

# 设置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ServiceManager:
    def __init__(self):
        self.processes: List[subprocess.Popen] = []
        self._shutdown_requested = False

    def start_flask_app(self):
        """启动Flask应用"""
        logger.info("启动Flask应用...")
        process = subprocess.Popen(
            [sys.executable, "app.py"], cwd=os.path.dirname(os.path.abspath(__file__))
        )
        self.processes.append(process)
        return process

    def start_celery_worker(self):
        """启动Celery worker"""
        logger.info("启动Celery worker...")
        process = subprocess.Popen(
            [sys.executable, "celery_worker.py"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )
        self.processes.append(process)
        return process

    def start_celery_beat(self):
        """启动Celery beat"""
        logger.info("启动Celery beat...")
        process = subprocess.Popen(
            [sys.executable, "celery_beat.py"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )
        self.processes.append(process)
        return process

    def shutdown(self):
        """关闭所有服务"""
        if self._shutdown_requested:
            return

        self._shutdown_requested = True
        logger.info("开始关闭所有服务...")

        # 发送SIGTERM信号给所有进程
        for process in self.processes:
            try:
                if process.poll() is None:  # 进程还在运行
                    logger.info(f"发送SIGTERM信号给进程 {process.pid}")
                    process.terminate()
            except Exception as e:
                logger.error(f"发送SIGTERM信号失败: {e}")

        # 等待进程结束
        for i, process in enumerate(self.processes):
            try:
                logger.info(f"等待进程 {process.pid} 结束...")
                process.wait(timeout=10)  # 等待10秒
                logger.info(f"进程 {process.pid} 已结束")
            except subprocess.TimeoutExpired:
                logger.warning(f"进程 {process.pid} 未在10秒内结束，强制终止")
                process.kill()
            except Exception as e:
                logger.error(f"等待进程结束时出错: {e}")

        logger.info("所有服务已关闭")

    def signal_handler(self, signum, frame):
        """信号处理器"""
        logger.info(f"收到信号 {signum}")
        self.shutdown()
        sys.exit(0)

    def monitor_processes(self):
        """监控进程状态"""
        while not self._shutdown_requested:
            for process in self.processes[:]:  # 使用切片创建副本
                if process.poll() is not None:  # 进程已结束
                    logger.warning(f"进程 {process.pid} 意外结束")
                    self.processes.remove(process)
            time.sleep(1)

    def run(self):
        """运行所有服务"""
        # 注册信号处理器
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        try:
            # 启动所有服务
            self.start_flask_app()
            time.sleep(2)  # 等待Flask应用启动

            self.start_celery_worker()
            time.sleep(1)  # 等待worker启动

            self.start_celery_beat()
            time.sleep(1)  # 等待beat启动

            logger.info("所有服务已启动")

            # 监控进程
            self.monitor_processes()

        except KeyboardInterrupt:
            logger.info("收到键盘中断")
        except Exception as e:
            logger.error(f"启动服务时出错: {e}")
        finally:
            self.shutdown()


def main():
    """主函数"""
    manager = ServiceManager()
    manager.run()


if __name__ == "__main__":
    main()
