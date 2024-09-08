from django.core.management.base import BaseCommand
import pika
import json
from concurrent.futures import ThreadPoolExecutor
from api.message_handlers import handle_book_update
from api.connections import rabbitmq_client
import threading



class Command(BaseCommand):
    help = 'Consumes messages for book updates, user updates, and book borrowings concurrently using ThreadPoolExecutor'

    def handle(self, *args, **options):
        self.start_consumers()


    def start_consumers(self):
        thread = threading.Thread(target=rabbitmq_client.consume_messages, args=('book_updates', handle_book_update))
        thread.daemon = True
        thread.start()

        # Wait for the thread to complete, or keep the main thread alive
        thread.join()  # Remove this if you want other operations to run concurrently in the main thread

        # To keep the command running, you can use a simple loop
        try:
            while True:
                continue  # Keep the main thread alive
        except KeyboardInterrupt:
            print("Received shutdown signal, exiting.")

