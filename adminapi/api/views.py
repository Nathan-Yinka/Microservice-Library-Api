from rest_framework import generics
from .models import Book, User, BorrowedBook
from .serializers import BookSerializer, UserSerializer, UserBorrowedBookSerializer, BorrowedBookSerializer, BookCreateSerializer

class BookListCreateView(generics.ListCreateAPIView):
    """
    List all books or create a new book.
    """
    queryset = Book.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookCreateSerializer
        return BookSerializer


class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a book instance.
    """
    serializer_class = BookSerializer
    queryset = Book.objects.all()

class UserListView(generics.ListAPIView):
    """
    List all registered users.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserBorrowedBook(generics.ListAPIView):
    """
    List users and their borrowed books.
    """
    queryset = User.objects.all().prefetch_related("borrowed_books__book")
    serializer_class = UserBorrowedBookSerializer

class BorrowedBookListView(generics.ListAPIView):
    """
    List borrowed books not yet returned.
    """
    serializer_class = BorrowedBookSerializer
    queryset = BorrowedBook.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(is_returned=False)
