import atexit
import os
import signal
import sys

debug = os.environ.get("DEBUG", "false").lower() in ("true", "1", "t")
if not debug:
    from gevent import monkey

    # monkey.patch_all()

import sys
import logging
import threading
from api.config import Config
from api.extensions import (
    database,
    redis,
    celery,
    mail,
    login,
    sentry,
    storage,
    migrate,
    wechat,
    # qrcode_api,
    limiter,
    rabbitmq,
)

from api.utils.decorator import api_json, debug_allowed
from flask import Flask, make_response, request, url_for
from api.libs.helper import has_no_empty_params
from api.commands import register_command


class ApiApp(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._shutdown_handlers = []

    def register_shutdown_handler(self, handler):
        """注册关闭时的清理函数"""
        self._shutdown_handlers.append(handler)

    def shutdown(self):
        """优雅关闭应用"""
        logging.info("开始优雅关闭应用...")
        for handler in self._shutdown_handlers:
            try:
                handler()
            except Exception as e:
                logging.error(f"关闭处理器执行失败: {e}")
        logging.info("应用关闭完成")


def create_app(config=None):
    app = ApiApp(__name__)

    if config is not None:
        app.config.from_object(config)
    else:
        app.config.from_object(Config())

    app.secret_key = app.config["SECRET_KEY"]

    logging.basicConfig(level=app.config.get("LOG_LEVEL", "INFO"))

    url_prefix = app.config.get("URL_PREFIX", "/api/v1")

    initialize_extension(app)
    register_handler(app)
    register_debug_route(app)
    register_blueprint(app, url_prefix=url_prefix)
    # register_scheduler(app)

    register_command(app)

    # 注册atexit处理器
    atexit.register(lambda: app.shutdown())

    return app


def initialize_extension(app):
    """初始化扩展，添加超时和错误处理"""
    import time

    extensions_to_init = [
        ("database", database),
        ("redis", redis),
        ("celery", celery),
        ("login", login),
        ("mail", mail),
        ("sentry", sentry),
        ("storage", storage),
        ("wechat", wechat),
        ("migrate", migrate),
        ("limiter", limiter),
        ("rabbitmq", rabbitmq),
    ]

    for name, extension in extensions_to_init:
        try:
            logging.info(f"初始化扩展: {name}")
            start_time = time.time()
            extension.init_app(app)
            elapsed = time.time() - start_time
            logging.info(f"扩展 {name} 初始化完成，耗时: {elapsed:.2f}秒")
        except Exception as e:
            logging.error(f"扩展 {name} 初始化失败: {e}")
            # 对于非关键扩展，继续初始化其他扩展
            if name in ["database", "redis"]:
                raise  # 关键扩展失败时抛出异常
            else:
                logging.warning(f"跳过扩展 {name} 的初始化")

    # 注册扩展的关闭处理器
    app.register_shutdown_handler(lambda: close_extensions(app))


def close_extensions(app):
    """关闭所有扩展"""
    logging.info("关闭扩展...")

    # 关闭Celery
    try:
        if "celery" in app.extensions:
            celery_app = app.extensions["celery"]
            # 使用新的关闭方法
            if hasattr(celery_app, "shutdown"):
                celery_app.shutdown()
            elif hasattr(celery_app, "control"):
                celery_app.control.shutdown()
            logging.info("Celery已关闭")
    except Exception as e:
        logging.error(f"关闭Celery时出错: {e}")

    # 关闭RabbitMQ连接
    try:
        if hasattr(rabbitmq, "mq_proxy"):
            rabbitmq.mq_proxy.close()
            logging.info("RabbitMQ连接已关闭")
    except Exception as e:
        logging.error(f"关闭RabbitMQ时出错: {e}")

    # 关闭Redis连接
    try:
        if hasattr(redis, "redis_client"):
            redis.redis_client.close()
            logging.info("Redis连接已关闭")
    except Exception as e:
        logging.error(f"关闭Redis时出错: {e}")

    # 关闭数据库连接
    try:
        if hasattr(database, "db"):
            database.db.session.close()
            database.db.engine.dispose()
            logging.info("数据库连接已关闭")
    except Exception as e:
        logging.error(f"关闭数据库时出错: {e}")


def register_handler(app):
    from .extensions.login import login_manager

    @login_manager.request_loader
    def load_account(request_from_flask_login):
        auth_header = request.headers.get("Authorization", "")
        if request.blueprint == "console":
            pass

    @login_manager.unauthorized_handler
    @api_json(status=401)
    def unauthorized():
        return {"code": "unauthorized", "message": "Unauthorized."}

    @app.after_request
    def after_request(response):
        response.headers.add("X-Version", app.config["CURRENT_VERSION"])
        response.headers.add("X-Env", app.config["DEPLOY_ENV"])

        return response

    @app.after_request
    def db_process(response):
        from .extensions.database import db

        if response.status_code < 400:
            db.session.commit()
        else:
            db.session.rollback()

        return response


def register_debug_route(app):
    @app.route("/health")
    @api_json()
    def health():
        """简化的健康检查，避免阻塞"""
        try:
            return {"status": "ok", "version": app.config["CURRENT_VERSION"]}
        except Exception as e:
            logging.error(f"健康检查失败: {e}")
            return {"status": "error", "message": str(e)}, 500

    @app.route("/threads")
    @debug_allowed
    @api_json()
    def threads():
        threads = threading.enumerate()
        threads = [
            {
                "name": thread.name,
                "id": thread.ident,
                "is_alive": thread.is_alive(),
            }
            for thread in threads
        ]
        return {"threads": threads}

    @app.route("/trace/:thread_id")
    @debug_allowed
    def trace(thread_id):
        import traceback

        stacktrace = traceback.format_stack(sys._current_frames()[thread_id])
        return make_response(stacktrace, 200)

    @app.route("/db-pool-stat")
    @debug_allowed
    @api_json()
    def pool_stat():
        from extensions.database import db

        engine = db.engine
        return {
            "pool_size": engine.pool.size(),
            "checked_in_connections": engine.pool.checkedin(),
            "checked_out_connections": engine.pool.checkedout(),
            "overflow_connections": engine.pool.overflow(),
            "connection_timeout": engine.pool.timeout(),
            "recycle_time": db.engine.pool._recycle,
        }

    @app.route("/sitemap")
    @debug_allowed
    @api_json()
    def site_map():
        links = []
        for rule in app.url_map.iter_rules():
            if "GET" in rule.methods and has_no_empty_params(rule):
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                links.append((url, rule.endpoint))
        return {"links": links}


def register_blueprint(app, url_prefix="/api/v1"):
    from .controllers.service_api import bp as service_api_bp
    from .controllers.web import bp as web_bp

    app.register_blueprint(service_api_bp, url_prefix=url_prefix)
    app.register_blueprint(web_bp, url_prefix=url_prefix)


# def register_scheduler(app):
#     with app.app_context():
#         from .scheduler.cleanup_scheduler import scheduler

#         scheduler.start()
#         atexit.register(lambda: scheduler.shutdown())


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5060)
