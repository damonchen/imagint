import os
import json
import dotenv

dotenv.load_dotenv()

DEFAULTS = {
    "DEBUG": "True",
    "DEBUG_ALLOWED_IP": "127.0.0.1",
    "SECRET_KEY": "b91f12b152edc98326d328e0f3014042",
    "DB_USERNAME": "imgint",
    "DB_PASSWORD": "c41ffdedf996e561181b055e242f6759",
    "DB_HOST": "localhost",
    "DB_PORT": "5434",
    "DB_DATABASE": "imgint",
    "DB_CHARSET": "",
    "REDIS_HOST": "localhost",
    "REDIS_PORT": "6379",
    "REDIS_DB": "0",
    "REDIS_USE_SSL": "False",
    "REDIS_PASSWORD": "eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81",
    "OAUTH_REDIRECT_PATH": "/console/api/oauth/authorize",
    "OAUTH_REDIRECT_INDEX_PATH": "/",
    "CONSOLE_WEB_URL": "https://cloud.qr.yihciyu.com",
    "CONSOLE_API_URL": "https://cloud.qr.yihciyu.com",
    "SERVICE_API_URL": "https://api.qr.yihciyu.com",
    # "APP_WEB_URL": "https://app.qr.yihciyu.com",
    "APP_WEB_URL": "http://127.0.0.1:5060",
    "FILES_URL": "",
    "S3_ADDRESS_STYLE": "auto",
    "STORAGE_TYPE": "local",
    "STORAGE_LOCAL_PATH": "storage",
    "CHECK_UPDATE_URL": "https://updates.qr.yihciyu.com",
    "DEPLOY_ENV": "PRODUCTION",
    "SQLALCHEMY_POOL_SIZE": 30,
    "SQLALCHEMY_MAX_OVERFLOW": 10,
    "SQLALCHEMY_POOL_RECYCLE": 3600,
    "SQLALCHEMY_ECHO": "False",
    "SENTRY_TRACES_SAMPLE_RATE": 1.0,
    "SENTRY_PROFILES_SAMPLE_RATE": 1.0,
    "WEAVIATE_GRPC_ENABLED": "True",
    "WEAVIATE_BATCH_SIZE": 100,
    "QDRANT_CLIENT_TIMEOUT": 20,
    "CELERY_BACKEND": "database",
    "LOG_LEVEL": "INFO",
    "CLEAN_DAY_SETTING": 30,
    "UPLOAD_FILE_SIZE_LIMIT": 15,
    "UPLOAD_FILE_BATCH_LIMIT": 5,
    "UPLOAD_IMAGE_FILE_SIZE_LIMIT": 10,
    "UPLOAD_TEMP_FOLDER": "/tmp",
    "UPLOAD_PERM_FOLDER": "/data/uploads",
    "TEMP_FILE_EXPIRY": 3600 * 24,
    "ALLOWED_IMAGE_EXTENSIONS": "png,jpg,jpeg,gif,bmp,webp",
    "OUTPUT_MODERATION_BUFFER_SIZE": 300,
    "MULTIMODAL_SEND_IMAGE_FORMAT": "base64",
    "INVITE_EXPIRY_HOURS": 72,
    "BILLING_ENABLED": "False",
    "CAN_REPLACE_LOGO": "False",
    "ETL_TYPE": "qrcode",
    "KEYWORD_STORE": "jieba",
    "BATCH_UPLOAD_LIMIT": 20,
    "CODE_EXECUTION_ENDPOINT": "",
    "CODE_EXECUTION_API_KEY": "",
    "TOOL_ICON_CACHE_MAX_AGE": 3600,
    "MILVUS_DATABASE": "default",
    "KEYWORD_DATA_SOURCE_TYPE": "database",
    "MAIL_TYPE": "mailgun",
    "MAILGUN_API_USERNAME": "",
    "MAILGUN_API_PASSWORD": "",
    "MAIL_API_DOMAIN": "",
    "CELERY_BROKER_URL": "redis://:eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81@localhost:6379/0",
    "CELERY_BACKEND": "redis",
    "CELERY_RESULT_BACKEND": "redis",
    "RABBITMQ_HOST": "localhost",
    "RABBITMQ_PORT": 5672,
    "RABBITMQ_USER": "imgint",
    "RABBITMQ_PASS": "password",
    "RABBITMQ_VHOST": "imgint",
    "RABBITMQ_EXCHANGE": "imgint.exchange",
    "RABBITMQ_ROUTING_KEY": "all",
    "RABBITMQ_QUEUE": "imgint.queue",
    "AES_KEY": "1c6a542248cad06516836644a354abe0",
    "SIGN_KEY": "0e87696d68db81809176990cb33dda47",
}


def get_env(key, default=""):
    return os.environ.get(key, DEFAULTS.get(key, default))


def get_bool_env(key):
    value = get_env(key)
    return value.lower() == "true" if value is not None else False


def get_list_env(key):
    value = get_env(key)
    return value.split(",") if value is not None else []


def get_cors_allow_origins(env, default):
    cors_allow_origins = []
    if get_env(env):
        for origin in get_env(env).split(","):
            cors_allow_origins.append(origin)
    else:
        cors_allow_origins = [default]

    return cors_allow_origins


class Config:
    """Application configuration class."""

    def __init__(self):
        # ------------------------
        # General Configurations.
        # ------------------------
        self.CURRENT_VERSION = "0.0.1"
        self.COMMIT_SHA = get_env("COMMIT_SHA")
        self.EDITION = "SELF_HOSTED"
        self.DEPLOY_ENV = get_env("DEPLOY_ENV")
        self.TESTING = False
        self.LOG_LEVEL = get_env("LOG_LEVEL")
        self.DEBUG = get_bool_env("DEBUG")
        self.DEBUG_ALLOWED_IP = get_env("DEBUG_ALLOWED_IP")

        # The backend URL prefix of the console API.
        # used to concatenate the login authorization callback or notion integration callback.
        self.CONSOLE_API_URL = get_env("CONSOLE_API_URL")

        # The front-end URL prefix of the console web.
        # used to concatenate some front-end addresses and for CORS configuration use.
        self.CONSOLE_WEB_URL = get_env("CONSOLE_WEB_URL")

        # WebApp Url prefix.
        # used to display WebAPP API Base Url to the front-end.
        self.APP_WEB_URL = get_env("APP_WEB_URL")

        # Service API Url prefix.
        # used to display Service API Base Url to the front-end.
        self.SERVICE_API_URL = get_env("SERVICE_API_URL")

        # File preview or download Url prefix.
        # used to display File preview or download Url to the front-end or as Multi-model inputs;
        # Url is signed and has expiration time.
        self.FILES_URL = (
            get_env("FILES_URL") if get_env("FILES_URL") else self.CONSOLE_API_URL
        )

        # Your App secret key will be used for securely signing the session cookie
        # Make sure you are changing this key for your deployment with a strong key.
        # You can generate a strong key using `openssl rand -base64 42`.
        # Alternatively you can set it with `SECRET_KEY` environment variable.
        self.SECRET_KEY = get_env("SECRET_KEY")

        # cors settings
        self.CONSOLE_CORS_ALLOW_ORIGINS = get_cors_allow_origins(
            "CONSOLE_CORS_ALLOW_ORIGINS", self.CONSOLE_WEB_URL
        )
        self.WEB_API_CORS_ALLOW_ORIGINS = get_cors_allow_origins(
            "WEB_API_CORS_ALLOW_ORIGINS", "*"
        )

        # check update url
        self.CHECK_UPDATE_URL = get_env("CHECK_UPDATE_URL")

        # ------------------------
        # Database Configurations.
        # ------------------------
        db_credentials = {
            key: get_env(key)
            for key in [
                "DB_USERNAME",
                "DB_PASSWORD",
                "DB_HOST",
                "DB_PORT",
                "DB_DATABASE",
                "DB_CHARSET",
            ]
        }

        db_extras = (
            f"?client_encoding={db_credentials['DB_CHARSET']}"
            if db_credentials["DB_CHARSET"]
            else ""
        )

        self.SQLALCHEMY_DATABASE_URI = f"postgresql://{db_credentials['DB_USERNAME']}:{db_credentials['DB_PASSWORD']}@{db_credentials['DB_HOST']}:{db_credentials['DB_PORT']}/{db_credentials['DB_DATABASE']}{db_extras}"
        self.SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_size": int(get_env("SQLALCHEMY_POOL_SIZE")),
            "max_overflow": int(get_env("SQLALCHEMY_MAX_OVERFLOW")),
            "pool_recycle": int(get_env("SQLALCHEMY_POOL_RECYCLE")),
        }

        self.SQLALCHEMY_ECHO = get_bool_env("SQLALCHEMY_ECHO")

        # ------------------------
        # Redis Configurations.
        # ------------------------
        self.REDIS_HOST = get_env("REDIS_HOST")
        self.REDIS_PORT = get_env("REDIS_PORT")
        self.REDIS_USERNAME = get_env("REDIS_USERNAME")
        self.REDIS_PASSWORD = get_env("REDIS_PASSWORD")
        self.REDIS_DB = get_env("REDIS_DB")
        self.REDIS_USE_SSL = get_bool_env("REDIS_USE_SSL")

        # ------------------------
        # Celery worker Configurations.
        # ------------------------
        self.CELERY_BROKER_URL = get_env("CELERY_BROKER_URL")
        self.CELERY_BACKEND = get_env("CELERY_BACKEND")
        self.CELERY_RESULT_BACKEND = (
            "db+{}".format(self.SQLALCHEMY_DATABASE_URI)
            if self.CELERY_BACKEND == "database"
            else self.CELERY_BROKER_URL
        )
        self.BROKER_USE_SSL = self.CELERY_BROKER_URL.startswith("rediss://")

        # ------------------------
        # File Storage Configurations.
        # ------------------------
        self.STORAGE_TYPE = get_env("STORAGE_TYPE")
        self.STORAGE_LOCAL_PATH = get_env("STORAGE_LOCAL_PATH")
        self.S3_ENDPOINT = get_env("S3_ENDPOINT")
        self.S3_BUCKET_NAME = get_env("S3_BUCKET_NAME")
        self.S3_ACCESS_KEY = get_env("S3_ACCESS_KEY")
        self.S3_SECRET_KEY = get_env("S3_SECRET_KEY")
        self.S3_REGION = get_env("S3_REGION")
        self.S3_ADDRESS_STYLE = get_env("S3_ADDRESS_STYLE")
        self.AZURE_BLOB_ACCOUNT_NAME = get_env("AZURE_BLOB_ACCOUNT_NAME")
        self.AZURE_BLOB_ACCOUNT_KEY = get_env("AZURE_BLOB_ACCOUNT_KEY")
        self.AZURE_BLOB_CONTAINER_NAME = get_env("AZURE_BLOB_CONTAINER_NAME")
        self.AZURE_BLOB_ACCOUNT_URL = get_env("AZURE_BLOB_ACCOUNT_URL")

        # ------------------------
        # Vector Store Configurations.
        # Currently, only support: qdrant, milvus, zilliz, weaviate
        # ------------------------
        self.VECTOR_STORE = get_env("VECTOR_STORE")
        self.KEYWORD_STORE = get_env("KEYWORD_STORE")
        # qdrant settings
        self.QDRANT_URL = get_env("QDRANT_URL")
        self.QDRANT_API_KEY = get_env("QDRANT_API_KEY")
        self.QDRANT_CLIENT_TIMEOUT = get_env("QDRANT_CLIENT_TIMEOUT")

        # milvus / zilliz setting
        self.MILVUS_HOST = get_env("MILVUS_HOST")
        self.MILVUS_PORT = get_env("MILVUS_PORT")
        self.MILVUS_USER = get_env("MILVUS_USER")
        self.MILVUS_PASSWORD = get_env("MILVUS_PASSWORD")
        self.MILVUS_SECURE = get_env("MILVUS_SECURE")
        self.MILVUS_DATABASE = get_env("MILVUS_DATABASE")

        # weaviate settings
        self.WEAVIATE_ENDPOINT = get_env("WEAVIATE_ENDPOINT")
        self.WEAVIATE_API_KEY = get_env("WEAVIATE_API_KEY")
        self.WEAVIATE_GRPC_ENABLED = get_bool_env("WEAVIATE_GRPC_ENABLED")
        self.WEAVIATE_BATCH_SIZE = int(get_env("WEAVIATE_BATCH_SIZE"))

        # ------------------------
        # Mail Configurations.
        # ------------------------
        # self.MAIL_TYPE = get_env("MAIL_TYPE")
        # self.MAILGUN_API_USERNAME = get_env("MAILGUN_API_USERNAME")
        # self.MAILGUN_API_PASSWORD = get_env("MAILGUN_API_PASSWORD")
        # self.MAIL_API_DOMAIN = get_env("MAIL_API_DOMAIN")

        self.MAIL_DEFAULT_SEND_FROM = get_env("MAIL_DEFAULT_SEND_FROM")

        self.RESEND_API_KEY = get_env("RESEND_API_KEY")
        self.RESEND_API_URL = get_env("RESEND_API_URL")

        # SMTP settings
        self.SMTP_SERVER = get_env("SMTP_SERVER")
        self.SMTP_PORT = get_env("SMTP_PORT")
        self.SMTP_USERNAME = get_env("SMTP_USERNAME")
        self.SMTP_PASSWORD = get_env("SMTP_PASSWORD")
        self.SMTP_USE_TLS = get_bool_env("SMTP_USE_TLS")

        # ------------------------
        # Workpace Configurations.
        # ------------------------
        self.INVITE_EXPIRY_HOURS = int(get_env("INVITE_EXPIRY_HOURS"))

        # ------------------------
        # Sentry Configurations.
        # ------------------------
        self.SENTRY_DSN = get_env("SENTRY_DSN")
        self.SENTRY_TRACES_SAMPLE_RATE = float(get_env("SENTRY_TRACES_SAMPLE_RATE"))
        self.SENTRY_PROFILES_SAMPLE_RATE = float(get_env("SENTRY_PROFILES_SAMPLE_RATE"))

        # ------------------------
        # Business Configurations.
        # ------------------------

        # multi model send image format, support base64, url, default is base64
        self.MULTIMODAL_SEND_IMAGE_FORMAT = get_env("MULTIMODAL_SEND_IMAGE_FORMAT")

        # Dataset Configurations.
        self.CLEAN_DAY_SETTING = get_env("CLEAN_DAY_SETTING")

        # File upload Configurations.
        self.UPLOAD_FILE_SIZE_LIMIT = int(get_env("UPLOAD_FILE_SIZE_LIMIT"))
        self.UPLOAD_FILE_BATCH_LIMIT = int(get_env("UPLOAD_FILE_BATCH_LIMIT"))
        self.UPLOAD_IMAGE_FILE_SIZE_LIMIT = int(get_env("UPLOAD_IMAGE_FILE_SIZE_LIMIT"))
        self.ALLOWED_IMAGE_EXTENSIONS = [
            key.lower() for key in get_list_env("ALLOWED_IMAGE_EXTENSIONS")
        ]
        self.UPLOAD_TEMP_FOLDER = get_env("UPLOAD_TEMP_FOLDER")
        self.UPLOAD_PERM_FOLDER = get_env("UPLOAD_PERM_FOLDER")
        self.TEMP_FILE_EXPIRY = int(get_env("TEMP_FILE_EXPIRY"))

        # Moderation in app Configurations.
        self.OUTPUT_MODERATION_BUFFER_SIZE = int(
            get_env("OUTPUT_MODERATION_BUFFER_SIZE")
        )

        # Notion integration setting
        self.NOTION_CLIENT_ID = get_env("NOTION_CLIENT_ID")
        self.NOTION_CLIENT_SECRET = get_env("NOTION_CLIENT_SECRET")
        self.NOTION_INTEGRATION_TYPE = get_env("NOTION_INTEGRATION_TYPE")
        self.NOTION_INTERNAL_SECRET = get_env("NOTION_INTERNAL_SECRET")
        self.NOTION_INTEGRATION_TOKEN = get_env("NOTION_INTEGRATION_TOKEN")

        self.ETL_TYPE = get_env("ETL_TYPE")
        self.UNSTRUCTURED_API_URL = get_env("UNSTRUCTURED_API_URL")
        self.BILLING_ENABLED = get_bool_env("BILLING_ENABLED")
        self.CAN_REPLACE_LOGO = get_bool_env("CAN_REPLACE_LOGO")

        self.BATCH_UPLOAD_LIMIT = get_env("BATCH_UPLOAD_LIMIT")

        self.CODE_EXECUTION_ENDPOINT = get_env("CODE_EXECUTION_ENDPOINT")
        self.CODE_EXECUTION_API_KEY = get_env("CODE_EXECUTION_API_KEY")

        self.API_COMPRESSION_ENABLED = get_bool_env("API_COMPRESSION_ENABLED")
        self.TOOL_ICON_CACHE_MAX_AGE = get_env("TOOL_ICON_CACHE_MAX_AGE")

        self.KEYWORD_DATA_SOURCE_TYPE = get_env("KEYWORD_DATA_SOURCE_TYPE")

        self.RABBITMQ_HOST = get_env("RABBITMQ_HOST")
        self.RABBITMQ_PORT = get_env("RABBITMQ_PORT")
        self.RABBITMQ_USER = get_env("RABBITMQ_USER")
        self.RABBITMQ_PASS = get_env("RABBITMQ_PASS")
        self.RABBITMQ_VHOST = get_env("RABBITMQ_VHOST")

        self.RABBITMQ_EXCHANGE = get_env("RABBITMQ_EXCHANGE")
        self.RABBITMQ_ROUTING_KEY = get_env("RABBITMQ_ROUTING_KEY")
        self.RABBITMQ_QUEUE = get_env("RABBITMQ_QUEUE")


        self.AES_KEY = get_env("AES_KEY")
        self.SIGN_KEY = get_env("SIGN_KEY")
