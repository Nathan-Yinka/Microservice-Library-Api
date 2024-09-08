from rest_framework import generics
from .models import Book, User, BorrowedBook
from .serializers import BookSerializer, UserSerializer, UserBorrowedBookSerializer, BorrowedBookSerializer

class BookListCreateView(generics.ListCreateAPIView):
    """
    Provides a list of all books and allows the creation of a new book.
    GET requests return a list of all books.
    POST requests allow adding a new book to the database.
    """
    serializer_class = BookSerializer
    queryset = Book.objects.all()

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Provides methods to retrieve, update, or delete a book instance.
    GET request retrieves a book by its ID.
    PUT and PATCH requests update the book details.
    DELETE request removes the book from the database.
    """
    serializer_class = BookSerializer
    queryset = Book.objects.all()

class UserListView(generics.ListAPIView):
    """
    Provides a list of all users in the library.
    GET request returns a list of all registered users.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserBorrowedBook(generics.ListAPIView):
    """
    Lists all users along with the books they have borrowed.
    This view utilizes nested serialization to include detailed information
    about borrowed books within each user's serialized data.
    """
    queryset = User.objects.all().prefetch_related("borrowed_books__book")
    serializer_class = UserBorrowedBookSerializer

class BorrowedBookListView(generics.ListAPIView):
    """
    Lists all borrowed books that have not been returned yet.
    Filter applied to show only the books currently borrowed.
    """
    serializer_class = BorrowedBookSerializer
    queryset = BorrowedBook.objects.all()

    def filter_queryset(self, queryset):
        queryset = queryset.filter(is_returned=False)
        return queryset