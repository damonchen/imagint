import pika
import json
import logging
import threading
import time
from typing import Callable, Optional, Dict, Any
from pika.exceptions import AMQPConnectionError, StreamLostError, ConnectionClosed

logger = logging.getLogger(__name__)


class RabbitMQService(object):
    def __init__(self, app=None):
        self.app = app
        self.channel = None
        self.connection = None
        self.parameters = None
        self.queues = []
        self._lock = threading.Lock()

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.channel = None
        self.connection = None

        if app is not None:
            # Get RabbitMQ configs from app config
            rabbitmq_host = app.config.get("RABBITMQ_HOST", "localhost")
            rabbitmq_port = app.config.get("RABBITMQ_PORT", 5672)
            rabbitmq_user = app.config.get("RABBITMQ_USER", "guest")
            rabbitmq_pass = app.config.get("RABBITMQ_PASS", "guest")
            rabbitmq_vhost = app.config.get("RABBITMQ_VHOST", "cchost")

            logger.info(
                f"RabbitMQ config: {rabbitmq_user} {rabbitmq_host} {rabbitmq_port} {rabbitmq_vhost}"
            )

            # SSL/TLS configuration if enabled
            ssl_options = None
            if app.config.get("RABBITMQ_SSL_ENABLED", False):
                ssl_options = pika.SSLOptions(
                    ca_certs=app.config.get("RABBITMQ_CA_CERTS"),
                    certfile=app.config.get("RABBITMQ_CERTFILE"),
                    keyfile=app.config.get("RABBITMQ_KEYFILE"),
                    verify_mode=app.config.get("RABBITMQ_VERIFY_MODE", "required"),
                )

            # Setup connection parameters
            credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
            self.parameters = pika.ConnectionParameters(
                host=rabbitmq_host,
                port=rabbitmq_port,
                virtual_host=rabbitmq_vhost,
                credentials=credentials,
                ssl_options=ssl_options,
                heartbeat=600,  # 10 minutes heartbeat
                blocked_connection_timeout=300,  # 5 minutes timeout
                connection_attempts=3,  # Retry connection 3 times
                retry_delay=5,  # 5 seconds between retries
            )

            # Store queues for reconnection
            self.queues = app.config.get("RABBITMQ_QUEUE", [])

            # Establish initial connection
            self._connect()

            # Register teardown callback
            app.teardown_appcontext(self.teardown)

    def _connect(self):
        """Establish connection to RabbitMQ with retry logic"""
        try:
            logger.info("Connecting to RabbitMQ...")
            self.connection = pika.BlockingConnection(self.parameters)
            self.channel = self.connection.channel()

            # Declare queues after connection
            self._declare(self.queues)

            logger.info("Successfully connected to RabbitMQ")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    def _ensure_connection(self):
        """Ensure connection is alive, reconnect if necessary"""
        with self._lock:
            try:
                if self.connection is None or self.connection.is_closed:
                    logger.warning(
                        "RabbitMQ connection lost, attempting to reconnect..."
                    )
                    self._connect()
                elif self.channel is None or self.channel.is_closed:
                    logger.warning("RabbitMQ channel lost, recreating...")
                    self.channel = self.connection.channel()
                    self._declare(self.queues)
            except Exception as e:
                logger.error(f"Failed to ensure RabbitMQ connection: {e}")
                raise

    def teardown(self, exception: Optional[Exception] = None):
        logger.info("Tearing down RabbitMQ connection and channel")
        with self._lock:
            if self.channel is not None:
                try:
                    self.channel.close()
                except Exception as e:
                    logger.error(f"Error closing channel: {e}")
                self.channel = None

            if self.connection is not None:
                try:
                    self.connection.close()
                except Exception as e:
                    logger.error(f"Error closing connection: {e}")
                self.connection = None

    def _declare(self, queues):
        """Declare exchanges and queues"""
        for queue in queues:
            name = queue["name"]
            self.channel.exchange_declare(name, exchange_type='direct', durable=True)
            for key in queue["keys"]:
                key = key.strip()
                self.queue_declare(f"{name}.{key}", True, exclusive=True)
                self.channel.queue_bind(exchange=f"{name}", queue=f'{name}.{key}', routing_key=key)

    def basic_publish(self, exchange: str, routing_key: str, body: bytes) -> None:
        """Publish message to specified channel with connection retry"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self._ensure_connection()

                self.channel.basic_qos(global_qos=1)

                properties = pika.spec.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE, priority=1,
                                                       content_type='text/plan')
                self.channel.basic_publish(
                    exchange=exchange, routing_key=routing_key, body=body, properties=properties,
                )
                logger.debug(
                    f"Successfully published message to {exchange}.{routing_key}"
                )
                return
            except (AMQPConnectionError, StreamLostError, ConnectionClosed) as e:
                logger.warning(
                    f"RabbitMQ connection error on attempt {attempt + 1}: {e}"
                )
                if attempt == max_retries - 1:
                    logger.error(
                        f"Failed to publish message after {max_retries} attempts"
                    )
                    raise
                time.sleep(1)  # Wait before retry
            except Exception as e:
                logger.error(f"Unexpected error publishing message: {e}")
                raise

    def basic_consume(
            self, queue: str, on_message_callback: Callable[[str], None]
    ) -> None:
        """Consume message from specified queue"""
        self._ensure_connection()
        self.channel.basic_consume(
            queue=queue, on_message_callback=on_message_callback, auto_ack=False
        )

    def queue_declare(self, queue: str, durable: bool = True, exclusive: bool = True) -> None:
        """Declare queue"""
        self._ensure_connection()
        self.channel.queue_declare(queue=queue, durable=durable, exclusive=exclusive)

    def start_consuming(self) -> None:
        """Start consuming messages"""
        self._ensure_connection()
        self.channel.start_consuming()

    def close(self):
        """Close connection and channel"""
        self.teardown()


mq_service = RabbitMQService()


def init_app(app):
    mq_service.init_app(app)
