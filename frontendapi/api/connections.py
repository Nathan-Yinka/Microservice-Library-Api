from django.conf import settings
import pika
import time
import json

class RabbitMQClient:
    """
    A client for managing connections and interactions with RabbitMQ. Handles connection retries, message publishing,
    and message consumption with robust error handling and connection management.
    """
    def __init__(self):
        """
        Initializes the RabbitMQClient with configurations pulled from Django settings.
        """
        self.host = settings.RABBITMQ_HOST
        self.port = settings.RABBITMQ_PORT
        self.username = settings.RABBITMQ_USERNAME
        self.password = settings.RABBITMQ_PASSWORD
        self.max_retries = settings.RABBITMQ_MAX_RETRIES
        self.delay = settings.RABBITMQ_RETRY_DELAY

    def _get_connection(self):
        """
        Attempts to establish a blocking connection to RabbitMQ with a retry mechanism.
        Retries a specified number of times with a delay between attempts if the connection fails.
        """
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
        """
        Publishes a message to a specified RabbitMQ queue. Messages are made durable and can be serialized if they are dictionaries.
        """
        connection = self._get_connection()
        channel = connection.channel()
        channel.queue_declare(queue=queue, durable=True)

        if isinstance(message, dict):
            message = json.dumps(message)

        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=message,
            properties=pika.BasicProperties(**(properties or {"delivery_mode": 2}))
        )
        print(f"Message sent to {queue}: {message}")
        connection.close()

    def consume_messages(self, queue, callback):
        """
        Consumes messages from a specified RabbitMQ queue and processes them using a provided callback function.
        Acknowledges messages only if they are processed successfully.
        """
        connection = self._get_connection()
        channel = connection.channel()
        channel.queue_declare(queue=queue, durable=True)

        def on_message_callback(ch, method, properties, body):
            try:
                message = body.decode('utf-8')
                message = json.loads(message)
                print(f"Received message: {message}")
                callback(message)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                print(f"Error processing message: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue=queue, on_message_callback=on_message_callback)
        print(f"[*] Waiting for messages on {queue}. To exit press CTRL+C")
        channel.start_consuming()

# Instance creation
rabbitmq_client = RabbitMQClient()
