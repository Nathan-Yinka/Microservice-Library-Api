from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from datetime import timedelta
from django.utils import timezone
from .models import User, Book, BorrowedBook
from .serializers import UserSerializer, BookSerializer, BorrowedBookSerializer, BorrowBookSerializer

class UserCreateView(generics.CreateAPIView):
    """
    API endpoint that allows creation of a new user.
    Users are created with unique email addresses and their first and last names.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BookListView(generics.ListAPIView):
    """
    API endpoint that lists all books.
    Supports filtering by 'publisher' and 'category' through query parameters.
    Only available books are listed.
    """
    serializer_class = BookSerializer

    def get_queryset(self):
        """
        Retrieve the queryset of available books and filter it based on the
        'publisher' and 'category' query parameters if they are provided.
        """
        queryset = Book.available_books.all()
        publisher = self.request.query_params.get('publisher', None)
        category = self.request.query_params.get('category', None)
        if publisher:
            queryset = queryset.filter(publisher__icontains=publisher)
        if category:
            queryset = queryset.filter(category__icontains=category)
        return queryset

class BookRetrieveView(generics.RetrieveAPIView):
    """
    API endpoint that retrieves a single book by its ID.
    Provides detailed information about a specific book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BorrowBookView(generics.CreateAPIView):
    """
    API endpoint for borrowing books.
    Users specify the book by ID, their email, and the number of days they wish to borrow the book.
    This endpoint checks book availability, creates a borrow record, and updates book status.
    """
    serializer_class = BorrowBookSerializer
    queryset = BorrowedBook.objects.all()
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST request to borrow a book. Validates the request data, checks if the book is available,
        and creates a BorrowedBook entry with the specified return date. Marks the book as unavailable if borrowed.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_id = serializer.validated_data['book_id']
        user_email = serializer.validated_data['user_email']
        number_of_days = serializer.validated_data['number_of_days']
        
        try:
            book = Book.objects.get(id=book_id)
            user = User.objects.get(email=user_email)
            if book.available:
                borrow_date = timezone.now()
                return_date = borrow_date + timedelta(days=number_of_days)
                borrowed_book = BorrowedBook.objects.create(
                    user=user,
                    book=book,
                    number_of_days=number_of_days,
                    return_date=return_date.date()
                )
                
                book.available = False
                book.save()
                response_serializer = BorrowedBookSerializer(borrowed_book)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
            return Response({"error": "This book is not available for borrowing"}, status=status.HTTP_400_BAD_REQUEST)
            
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
