from django.conf import settings
import pika
import time
import json

class RabbitMQClient:
    def __init__(self):
        self.host = settings.RABBITMQ_HOST
        self.port = settings.RABBITMQ_PORT
        self.username = settings.RABBITMQ_USERNAME
        self.password = settings.RABBITMQ_PASSWORD
        self.max_retries = settings.RABBITMQ_MAX_RETRIES
        self.delay = settings.RABBITMQ_RETRY_DELAY

    def _get_connection(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        connection_params = pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials)

        for attempt in range(self.max_retries):
            try:
                return pika.BlockingConnection(connection_params)
            except pika.exceptions.AMQPConnectionError as e:
                if attempt < self.max_retries - 1:
                    print(f"Connection attempt {attempt + 1} failed: {e}. It appears RabbitMQ may not be fully started yet. Retrying in {self.delay} seconds...")
                    time.sleep(self.delay)
                else:
                    print("Max retries reached. Could not connect to RabbitMQ.")
                    raise

    def publish_message(self, message, queue, properties=None):
        connection = self._get_connection()
        channel = connection.channel()
        channel.queue_declare(queue=queue, durable=True)

        # Serialize message if it's a dictionary
        if isinstance(message, dict):
            message = json.dumps(message)

        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=message,
            properties=pika.BasicProperties(**(properties or {"delivery_mode":2}))
        )
        print(f"Message sent to {queue}: {message}")
        connection.close()

    def consume_messages(self, queue, callback):
        connection = self._get_connection()
        channel = connection.channel()
        channel.queue_declare(queue=queue, durable=True)

        def on_message_callback(ch, method, properties, body):
            try:
                message = body.decode('utf-8')
                message = json.loads(body)
                print(f"Received message: {message}")
                callback(message)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                print(f"Error processing message: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue=queue, on_message_callback=on_message_callback)
        print(f"[*] Waiting for messages on {queue}. To exit press CTRL+C")
        channel.start_consuming()


rabbitmq_client = RabbitMQClient()