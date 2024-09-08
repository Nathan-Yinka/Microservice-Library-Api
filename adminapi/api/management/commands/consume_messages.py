from django.core.management.base import BaseCommand
import threading
from api.message_handlers import handle_user_enrollment, handle_borrow_book
from api.connections import rabbitmq_client


class Command(BaseCommand):
    help = 'Consumes messages for book updates, user updates, and book borrowings concurrently using ThreadPoolExecutor'

    def handle(self, *args, **options):
        self.start_consumers()

    def start_consumers(self):
        # Start the thread for user updates
        user_thread = threading.Thread(target=rabbitmq_client.consume_messages, args=('user_updates', handle_user_enrollment))
        user_thread.daemon = True
        user_thread.start()

        borrow_thread = threading.Thread(target=rabbitmq_client.consume_messages, args=('borrow_updates', handle_borrow_book))
        borrow_thread.daemon = True 
        borrow_thread.start()

        try:
            while True:
                continue 
        except KeyboardInterrupt:
            print("Received shutdown signal, exiting.")