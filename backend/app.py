import signal
import sys
import logging
from api.api_app import create_app

# 设置日志
# logging.basicConfig(
#     level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )
logger = logging.getLogger(__name__)

app = create_app()


def signal_handler(signum, frame):
    """信号处理器"""
    logger.info(f"收到信号 {signum}，开始关闭Flask应用...")
    # Flask应用会在atexit中自动调用shutdown方法
    sys.exit(0)


if __name__ == "__main__":
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # kill

    logger.info("启动Flask应用...")
    try:
        app.run(host="0.0.0.0", port=5080, debug=False)
    except KeyboardInterrupt:
        logger.info("收到键盘中断，正在关闭...")
    except Exception as e:
        logger.error(f"Flask应用启动失败: {e}", sys.exc_info())
        sys.exit(1)
