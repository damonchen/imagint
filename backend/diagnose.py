#!/usr/bin/env python
"""
系统诊断脚本
检查系统状态和可能的问题
"""

import os
import sys
import time
import socket
import logging
import subprocess
from pathlib import Path

# 设置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def check_port_availability():
    """检查端口可用性"""
    logger.info("检查端口可用性...")

    ports_to_check = [5080, 6379, 5672, 5434]

    for port in ports_to_check:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = sock.connect_ex(("localhost", port))
            if result == 0:
                logger.warning(f"⚠ 端口 {port} 已被占用")
            else:
                logger.info(f"✓ 端口 {port} 可用")
        except Exception as e:
            logger.error(f"✗ 检查端口 {port} 时出错: {e}")
        finally:
            sock.close()


def check_docker_services():
    """检查Docker服务状态"""
    logger.info("检查Docker服务状态...")

    try:
        result = subprocess.run(
            ["docker", "ps"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            logger.info("✓ Docker服务运行正常")
            logger.info("运行中的容器:")
            for line in result.stdout.split("\n")[1:]:  # 跳过标题行
                if line.strip():
                    logger.info(f"  {line}")
        else:
            logger.warning("⚠ Docker服务可能有问题")
    except FileNotFoundError:
        logger.warning("⚠ Docker未安装或不在PATH中")
    except subprocess.TimeoutExpired:
        logger.error("✗ Docker命令超时")
    except Exception as e:
        logger.error(f"✗ 检查Docker服务时出错: {e}")


def check_environment_variables():
    """检查环境变量"""
    logger.info("检查环境变量...")

    # 检查当前工作目录
    logger.info(f"当前工作目录: {os.getcwd()}")

    # 检查Python路径
    logger.info(f"Python可执行文件: {sys.executable}")
    logger.info(f"Python版本: {sys.version}")

    # 检查关键环境变量
    env_vars = [
        "CELERY_BROKER_URL",
        "CELERY_BACKEND",
        "REDIS_HOST",
        "REDIS_PORT",
        "SQLALCHEMY_DATABASE_URI",
    ]

    for var in env_vars:
        value = os.environ.get(var)
        if value:
            logger.info(f"✓ {var}: {value}")
        else:
            logger.warning(f"⚠ {var}: 未设置")


def check_file_permissions():
    """检查文件权限"""
    logger.info("检查文件权限...")

    files_to_check = ["app.py", "api/api_app.py", "api/config.py"]

    for file_path in files_to_check:
        if os.path.exists(file_path):
            logger.info(f"✓ {file_path} 存在")
            try:
                with open(file_path, "r") as f:
                    f.read(100)  # 尝试读取前100个字符
                logger.info(f"✓ {file_path} 可读")
            except Exception as e:
                logger.error(f"✗ {file_path} 读取失败: {e}")
        else:
            logger.warning(f"⚠ {file_path} 不存在")


def test_network_connectivity():
    """测试网络连接"""
    logger.info("测试网络连接...")

    hosts_to_test = [
        ("localhost", 5080),
        ("localhost", 6379),
        ("localhost", 5672),
        ("localhost", 5434),
    ]

    for host, port in hosts_to_test:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 5秒超时
        try:
            result = sock.connect_ex((host, port))
            if result == 0:
                logger.info(f"✓ {host}:{port} 可连接")
            else:
                logger.warning(f"⚠ {host}:{port} 不可连接")
        except Exception as e:
            logger.error(f"✗ 测试 {host}:{port} 时出错: {e}")
        finally:
            sock.close()


def main():
    """主函数"""
    logger.info("=== 系统诊断开始 ===")

    check_environment_variables()
    check_file_permissions()
    check_port_availability()
    check_docker_services()
    test_network_connectivity()

    logger.info("=== 系统诊断完成 ===")

    print("\n" + "=" * 50)
    print("诊断建议:")
    print("1. 如果端口被占用，请停止相关服务")
    print("2. 如果Docker服务有问题，请检查Docker状态")
    print("3. 如果环境变量未设置，请检查配置文件")
    print("4. 如果网络连接有问题，请检查防火墙设置")
    print("=" * 50)


if __name__ == "__main__":
    main()
