from django.core.exceptions import ObjectDoesNotExist
from .models import Book

def handle_book_update(message):
    """
    Process incoming messages to manage book entries in the database based on the specified action.
    The function supports adding a new book, updating an existing one, or removing a book based on the message details.

    Args:
        message (dict): Contains the details of the book and the action ('add', 'update', 'remove') to be performed.

    The function logs the outcome of the operation, including any additions, updates, or deletions of book records.
    """
    action = message.pop('action') 
    book_id = message.get('id')

    if action in ['update', 'add']:
        book, created = Book.objects.update_or_create(
            id=book_id,
            defaults=message
        )
        if created:
            print(f"Added new book with ID {book_id}")
        else:
            print(f"Updated book with ID {book_id}")

    elif action == 'remove':
        try:
            book = Book.objects.get(id=book_id)
            book.delete()
            print(f"Removed book with ID {book_id}")
        except ObjectDoesNotExist:
            print(f"Book with ID {book_id} not found and could not be removed.")
