from django.core.exceptions import ObjectDoesNotExist
from .models import Book


def handle_book_update(message):
    """
    Handle messages to update the book database.
    Messages can instruct to add, update, or remove a book.
    """
    action = message.pop('action')
    book_id = message.get('id')

    if action == 'update' or action == 'add':
        # Use update_or_create to handle both adding and updating
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
            # Attempt to delete the book
            book = Book.objects.get(id=book_id)
            book.delete()
            print(f"Removed book with ID {book_id}")
        except ObjectDoesNotExist:
            print(f"Book with ID {book_id} not found and could not be removed.")
