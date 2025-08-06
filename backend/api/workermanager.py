import json
import threading
import pika
import requests
import argparse
import configparser
import subprocess
from concurrent.futures import ThreadPoolExecutor


class Config(object):
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.model_threads = self.config.getint('worker', 'model_threads')
        self.rabbitmq_host = self.config.get('rabbitmq', 'host')
        self.rabbitmq_port = self.config.getint('rabbitmq', 'port')
        self.rabbitmq_username = self.config.get('rabbitmq', 'username')
        self.rabbitmq_password = self.config.get('rabbitmq', 'password')
        self.api_url = self.config.get('api', 'url')
        self.api_key = self.config.get('api', 'key')

class WorkerManager(object):
    def __init__(self, config):
        self.config = config
        self.model_threads = self.config.model_threads
        self.executor = ThreadPoolExecutor(max_workers=self.model_threads)
        
        # RabbitMQ connection
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.rabbitmq_host, self.rabbitmq_port, self.rabbitmq_username, self.rabbitmq_password))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='model_queue')

    def process_message(self, message):
        try:
            # Parse message
            data = json.loads(message)
            model = data['model']
            chat_id = data['chat_id']
            user_plan = data['user_plan']
            message_id = data['message_id']
            prompt = data['prompt']
            params = data.get('params', {})

            # Start worker process
            process = subprocess.Popen(
                ["python3", f"workers/{model}_worker.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Send parameters to worker
            worker_input = json.dumps({
                "prompt": prompt,
                "params": params,
                "user_plan": user_plan,
            })
            stdout, stderr = process.communicate(input=worker_input)

            if stderr:
                print(f"Worker error: {stderr}")
                return

            # Parse worker response
            result = json.loads(stdout)
            
            # Send results back to API
            api_url = f"{self.config.api_url}/chat/{chat_id}/messages/{message_id}"
            requests.post(api_url, json={"images": result.get("images", [])}, headers={"Authorization": f"Bearer {self.config.api_key}"})

        except Exception as e:
            print(f"Error processing message: {e}")

    def callback(self, ch, method, properties, body):
        # Submit task to thread pool
        self.executor.submit(self.process_message, body.decode())
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        self.channel.basic_qos(prefetch_count=self.model_threads)
        self.channel.basic_consume(queue='model_queue', on_message_callback=self.callback)
        print("Worker manager started. Waiting for messages...")
        self.channel.start_consuming()

if __name__ == "__main__":
    # 读取配置文件，获取模型线程数，rabbitmq信息，以及api 服务地址，配置文件为ini文件格式？
    # 通过argparse来获取config文件位置
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='config.ini')
    args = parser.parse_args()

    config_file = args.config

    config = Config(config_file=config_file)

    manager = WorkerManager(config=config)
    manager.run()
