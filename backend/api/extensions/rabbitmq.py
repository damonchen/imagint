# import pika
# import json
# import logging
# import threading
# import time
# from typing import Callable, Optional, Dict, Any
# from pika.exceptions import AMQPConnectionError, StreamLostError, ConnectionClosed


# from pika import channel
# from pika import SelectConnection
# from pika import frame
# from pika import spec
# from pika import URLParameters
# from queue import Queue
# import time
# import functools
# import threading


# logger = logging.getLogger(__name__)


# class RMQ(threading.Thread):
#     """
#     This class is a simple RMQ consumer which can obtain queue size and allows consuming of messages.
#     To consume messages, you need to provide on_message callback to the class contructor.
#     """

#     def __init__(
#         self,
#         queueName: str,
#         exchangeName: str,
#         routing_key: str = "",
#         address: str = "",
#         on_message: callable = None,
#         on_queue_bind: callable = None,
#     ):
#         threading.Thread.__init__(self)
#         self._connection = None
#         self._channel = None
#         self._queue = queueName
#         self._exchange = exchangeName
#         self._address = address
#         self._exchange_type = "direct"
#         self._on_message_callback = (
#             on_message if on_message is not None else self.on_message_pass
#         )
#         self._on_queue_bind = (
#             on_queue_bind if on_queue_bind is not None else self.on_queue_bind
#         )
#         self._is_connected = False
#         self._shutdown = False
#         self._routing_key = routing_key
#         self._finished = False
#         self._reconnect_delay_s = 5

#     def on_message_pass(
#         self,
#         channel: channel.Channel,
#         method: spec.Basic.Deliver,
#         properties: spec.BasicProperties,
#         body: bytes,
#     ):
#         pass

#     def on_open_channel(self, channel: channel.Channel):
#         logger.debug("Channel setup success")
#         self._channel = channel
#         self._channel.add_on_close_callback(self.on_channel_closed)
#         self._channel.exchange_declare(
#             exchange=self._exchange,
#             exchange_type=self._exchange_type,
#             callback=self.on_exchange_declare,
#         )

#     def on_exchange_declare(self, unused_frame: frame.Method):
#         logger.debug("Declared exchange {}".format(self._exchange))
#         self._channel.queue_declare(
#             queue=self._queue, callback=self.on_queue_declare, durable=True
#         )

#     def on_queue_declare(self, method_frame: frame.Method):
#         logger.debug("Declared queue {}".format(self._queue))
#         self._channel.queue_bind(
#             queue=self._queue,
#             exchange=self._exchange,
#             routing_key=self._routing_key,
#             callback=self._on_queue_bind,
#         )
#         self._channel.add_on_cancel_callback(self.on_channel_cancelled)
#         # Call this if you want to start consuming messages. Note that you need to provied proper on_message callaback
#         # self._channel.basic_consume(
#         #    on_message_callback=self._on_message_callback,
#         #    queue=self._queue)

#     def on_channel_cancelled(self, method_frame: frame.Method):
#         logger.debug("Channel canceled")
#         if self._channel:
#             self._channel.close()

#     def on_queue_bind(self, unused_frame: frame.Method):
#         logger.debug(
#             "Queue {} bound to exchange {}".format(self._queue, self._exchange)
#         )
#         self._is_connected = True

#     def on_channel_closed(self, channel: channel.Channel, exception: Exception):
#         self._is_connected = False
#         logger.debug("Channel {} is closed".format(channel))
#         self._channel = None
#         if not self._shutdown:
#             logger.debug("Closing connection and reconnecting to channel")
#             self._connection.close()
#         else:
#             logger.debug("RMQ shutdown - channel")

#     def on_open_connection(self, connection: SelectConnection):
#         logger.debug("Connection opened")
#         self._channel = None
#         connection.channel(on_open_callback=self.on_open_channel)

#     def on_connection_closed(self, connection: SelectConnection, exception: Exception):
#         logger.debug("Connection closed: {}".format(str(exception)))
#         self._channel = None
#         if not self._shutdown:
#             logger.debug(
#                 "Reopening connection in {} seconds".format(self._reconnect_delay_s)
#             )
#         else:
#             logger.debug(f"RMQ shutdown - connection closed for queue {self._queue}")
#         self._connection.ioloop.stop()

#     def getQueueName(self) -> str:
#         return self._queue

#     def shutdown(self):
#         self._shutdown = True
#         logger.debug(f"Shutting down connection and channel for queue {self._queue}")
#         if self._channel is not None:
#             logger.debug("Closing channel")
#             self._channel.close()
#         if self._connection is not None:
#             logger.debug("Closing connection")
#             self._connection.close()

#     def connect(self):
#         parameters = URLParameters(self._address)

#         self._connection = SelectConnection(
#             on_open_callback=self.on_open_connection,
#             on_close_callback=self.on_connection_closed,
#             on_open_error_callback=self.on_open_error,
#             parameters=parameters,
#         )
#         self._connection.ioloop.start()

#     def on_open_error(self, connection: SelectConnection, exception: Exception):
#         logger.debug("Failed to open connection")
#         self._connection.ioloop.stop()

#     def wait_for_connection(self):
#         while not self._is_connected:
#             time.sleep(0.1)

#     def run(self):
#         self._finished = False
#         while not self._shutdown:
#             self.connect()
#             if not self._shutdown:
#                 time.sleep(self._reconnect_delay_s)
#         self._finished = True
#         logger.debug("Stopped")


# class RMQConsumer(RMQ):
#     def __init__(
#         self,
#         queueName: str,
#         exchangeName: str,
#         routing_key: str = "",
#         address: str = "",
#         on_message: callable = None,
#     ):
#         super().__init__(
#             queueName=queueName,
#             exchangeName=exchangeName,
#             routing_key=routing_key,
#             address=address,
#             on_message=on_message,
#         )
#         self.start()
#         self.wait_for_connection()
#         self.queue_size_ = -1

#     def on_queue_size(self, event: threading.Event, method_frame: frame.Method):
#         self.queue_size_ = method_frame.method.message_count
#         event.set()
#         logger.debug(f"on_queue_size for queue {self._queue}")

#     def on_queue_delete(self, event: threading.Event, method_frame: frame.Method):
#         if method_frame.method.NAME == "Queue.DeleteOk":
#             logger.debug("Deleted queue {}".format(self._queue))
#         else:
#             logger.debug("Failed to delete queue {}".format(self._queue))

#     def getQueueSize(self, timeout: int = 10) -> int:
#         self.queue_size_ = -1
#         if not self._is_connected or self._channel is None:
#             return self.queue_size_
#         event = threading.Event()
#         queue_size_event_callback = functools.partial(self.on_queue_size, event)
#         self._channel.queue_declare(
#             queue=self._queue, callback=queue_size_event_callback, durable=True
#         )
#         event.wait(timeout)
#         return self.queue_size_

#     def deleteQueue(self, timeout: int = 10):
#         # If we're not setup don't do anything
#         if not self._is_connected or self._channel is None:
#             return

#         event = threading.Event()
#         delete_event_callback = functools.partial(self.on_queue_delete, event)
#         logger.debug("Deleting queue {}".format(self._queue))
#         self._channel.queue_delete(queue=self._queue, callback=delete_event_callback)
#         event.wait(timeout)


# class RMQProducer(RMQ):
#     def __init__(
#         self,
#         queueName: str,
#         exchangeName: str,
#         routing_key: str = "",
#         address: str = "",
#     ):
#         super().__init__(
#             queueName=queueName,
#             exchangeName=exchangeName,
#             routing_key=routing_key,
#             address=address,
#         )

#         self.start()
#         self.wait_for_connection()

#     def publish(self, message: str):
#         logger.debug(f"Publishing message to {self._exchange}.{self._routing_key}")
#         if self._channel is not None:
#             self._channel.basic_publish(
#                 exchange=self._exchange, routing_key=self._routing_key, body=message
#             )


# class RabbitMQProxy(object):
#     def __init__(self, app=None):
#         self.app = app
#         self._consumer = None
#         self._producer = None

#         if app is not None:
#             self.init_app(app)

#     def init_app(self, app):
#         self.app = app
#         self.channel = None
#         self.connection = None

#         if app is not None:
#             # Get RabbitMQ configs from app config
#             rabbitmq_host = app.config.get("RABBITMQ_HOST", "localhost")
#             rabbitmq_port = app.config.get("RABBITMQ_PORT", 5672)
#             rabbitmq_user = app.config.get("RABBITMQ_USER", "guest")
#             rabbitmq_pass = app.config.get("RABBITMQ_PASS", "guest")
#             rabbitmq_vhost = app.config.get("RABBITMQ_VHOST", "cchost")

#             logger.info(
#                 f"RabbitMQ config: {rabbitmq_user} {rabbitmq_host} {rabbitmq_port} {rabbitmq_vhost}"
#             )

#             self.address = f"amqp://{rabbitmq_user}:{rabbitmq_pass}@{rabbitmq_host}:{rabbitmq_port}/{rabbitmq_vhost}"

#             # SSL/TLS configuration if enabled
#             ssl_options = None
#             if app.config.get("RABBITMQ_SSL_ENABLED", False):
#                 ssl_options = pika.SSLOptions(
#                     ca_certs=app.config.get("RABBITMQ_CA_CERTS"),
#                     certfile=app.config.get("RABBITMQ_CERTFILE"),
#                     keyfile=app.config.get("RABBITMQ_KEYFILE"),
#                     verify_mode=app.config.get("RABBITMQ_VERIFY_MODE", "required"),
#                 )

#             # Setup connection parameters
#             # credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
#             # self.parameters = pika.ConnectionParameters(
#             #     host=rabbitmq_host,
#             #     port=rabbitmq_port,
#             #     virtual_host=rabbitmq_vhost,
#             #     credentials=credentials,
#             #     ssl_options=ssl_options,
#             #     heartbeat=600,  # 10 minutes heartbeat
#             #     blocked_connection_timeout=300,  # 5 minutes timeout
#             #     connection_attempts=3,  # Retry connection 3 times
#             #     retry_delay=5,  # 5 seconds between retries
#             # )

#             # Store queues for reconnection
#             self.exchange_key = app.config.get("RABBITMQ_EXCHANGE", "")
#             self.routing_key = app.config.get("RABBITMQ_ROUTING_KEY", "")
#             self.queue = app.config.get("RABBITMQ_QUEUE", "")
#             self.queue_name = app.config.get("RABBITMQ_QUEUE_TYPE", "producer")

#             self._on_custom_message = None

#             if self.queue_name == "consumer":
#                 self._consumer = RMQConsumer(
#                     queueName=self.queue,
#                     exchangeName=self.exchange_key,
#                     routing_key=self.routing_key,
#                     address=self.address,
#                     on_message=self._on_message,
#                 )

#             if self.queue_name == "producer":
#                 self._producer = RMQProducer(
#                     queueName=self.queue,
#                     exchangeName=self.exchange_key,
#                     routing_key=self.routing_key,
#                     address=self.address,
#                 )

#     def _on_message(
#         self,
#         channel: channel.Channel,
#         method: spec.Basic.Deliver,
#         properties: spec.BasicProperties,
#         body: bytes,
#     ):
#         logger.debug(f"Received message: {body}")
#         if self._on_custom_message is not None:
#             self._on_custom_message(body)

#     def publish(self, message: str):
#         if self.queue_name == "producer":
#             self._producer.publish(message)

#     def consume(
#         self,
#         on_message: Callable[[str], None],
#     ):
#         if self.queue_name == "consumer":
#             self._on_custom_message = on_message

#     def close(self):
#         if self.queue_name == "consumer":
#             self._consumer.shutdown()
#         if self.queue_name == "producer":
#             self._producer.shutdown()


# mq_proxy = RabbitMQProxy()


# def init_app(app):
#     mq_proxy.init_app(app)
