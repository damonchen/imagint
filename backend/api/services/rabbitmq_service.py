# import logging
# import json
# from typing import Callable
# from api.extensions.rabbitmq import mq_proxy

# logger = logging.getLogger(__name__)


# class RabbitMQService(object):
#     @staticmethod
#     def publish_task(payload: dict) -> None:
#         """
#         Publish task message to RabbitMQ
#         Args:
#             exchange: Exchange name
#             key: Routing key
#             payload: Message payload
#         """
#         try:
#             message = json.dumps(payload)
#             mq_proxy.publish(
#                 message
#             )
#         except Exception as e:
#             logger.error(f"Failed to publish task message: {e}")
#             raise

#     @staticmethod
#     def consume_task(on_message_callback: Callable[[str], None]) -> None:
#         """
#         Consume task message from RabbitMQ
#         Args:
#             queue: Queue name
#             on_message_callback: Callback function to handle the message
#         """
#         mq_proxy.consume(on_message=on_message_callback)
