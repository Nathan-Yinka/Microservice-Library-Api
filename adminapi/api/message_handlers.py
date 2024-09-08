from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .models import Book, User, BorrowedBook

def handle_user_enrollment(message):
    """
    Processes user enrollment or updates based on the provided message.
    Creates or updates a user entry with the provided email and additional details.

    Args:
        message (dict): A dictionary containing user details with keys like 'email' and other user attributes.

    If a new user is created or an existing user is updated, it logs the action.
    """
    try:
        user, created = User.objects.update_or_create(
            email=message['email'],
            defaults=message
        )
        if created:
            print(f"New user enrolled with email: {message['email']}")
        else:
            print(f"User updated with email: {message['email']}")
    except IntegrityError as e:
        print(f"Failed to process user enrollment/update: {str(e)}")
        
        
        
def handle_borrow_book(message):
    """
    Handles book borrowing and returning based on the status in the message.
    For borrowing, it updates or creates a borrow record and marks the book as unavailable.
    For returning, it updates the borrow record and marks the book as available.

    Args:
        message (dict): A dictionary with keys 'user_id', 'book_id', 'status', and other transaction details.

    Logs actions and errors related to book transactions.
    """
    try:
        user = User.objects.get(id=message['user_id'])
        book = Book.objects.get(id=message['book_id'])

        if message['status'] == 'borrow':
            borrow_record, created = BorrowedBook.objects.update_or_create(
                id=message['id'],
                user=user,
                book=book,
                defaults={
                    'borrowed_on': message['borrowed_on'],
                    'return_date': message['return_date'],
                    'number_of_days': message['number_of_days'],
                    'is_returned': False
                }
            )
            if created:
                book.available = False
                book.save()
                print(f"Book {book.id} borrowed by User {user.email}")
            else:
                print(f"Borrow record updated for Book {book.id} by User {user.email}")

        elif message['status'] == 'return':
            borrow_record = BorrowedBook.objects.get(user=user, book=book)
            borrow_record.is_returned = True
            borrow_record.save()
            book.available = True
            book.save()
            print(f"Book {book.id} returned by User {user.id}")

    except ObjectDoesNotExist as e:
        print(f"Error processing book transaction: {str(e)}")
    except IntegrityError as e:
        print(f"Database integrity error: {str(e)}")
