from django.core.management.base import BaseCommand
import pika
import json
from concurrent.futures import ThreadPoolExecutor
from api.message_handlers import handle_user_enrollment, handle_borrow_book
from api.connections import RabbitMQClient
import threading
from api.connections import rabbitmq_client


class Command(BaseCommand):
    help = 'Consumes messages for book updates, user updates, and book borrowings concurrently using ThreadPoolExecutor'

    def handle(self, *args, **options):
        self.start_consumers()

    def start_consumers(self):
        # Start the thread for user updates
        user_thread = threading.Thread(target=rabbitmq_client.consume_messages, args=('user_updates', handle_user_enrollment))
        user_thread.daemon = True  # Ensures thread exits when main process does
        user_thread.start()

        # Start the thread for borrow book updates
        borrow_thread = threading.Thread(target=rabbitmq_client.consume_messages, args=('borrow_updates', handle_borrow_book))
        borrow_thread.daemon = True  # Ensures thread exits when main process does
        borrow_thread.start()

        # To keep the command running, you can use a simple loop
        try:
            while True:
                # This loop will keep the main thread alive to allow daemon threads to run
                continue 
        except KeyboardInterrupt:
            print("Received shutdown signal, exiting.")