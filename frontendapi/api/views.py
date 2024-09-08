from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from datetime import timedelta
from django.utils import timezone
from .models import User, Book, BorrowedBook
from .serializers import UserSerializer, BookSerializer, BorrowedBookSerializer, BorrowBookSerializer

class UserCreateView(generics.CreateAPIView):
    """
    Create a new user with a unique email, first name, and last name.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BookListView(generics.ListAPIView):
    """
    List all available books, filterable by 'publisher' and 'category'.
    """
    serializer_class = BookSerializer

    def get_queryset(self):
        """
        Filter available books by 'publisher' and 'category' if provided.
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
    Retrieve detailed information about a book by its ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BorrowBookView(generics.CreateAPIView):
    """
    Borrow a book by specifying the book ID, user email, and borrowing duration.
    Ensures book availability, creates a borrow record, and updates book status.
    """
    serializer_class = BorrowBookSerializer
    queryset = BorrowedBook.objects.all()
    
    def post(self, request, *args, **kwargs):
        """
        Validate request, check book availability, create BorrowedBook entry with return date, and mark the book as unavailable.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_id = serializer.validated_data['book_id']
        user_email = serializer.validated_data['user_email']
        number_of_days = serializer.validated_data['number_of_days']
        
        book = get_object_or_404(Book, id=book_id)
        user = get_object_or_404(User, email=user_email)
        
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
