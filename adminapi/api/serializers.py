# serializers.py
from rest_framework import serializers
from .models import Book, User,BorrowedBook

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        
class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ['available']
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class BorrowedBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True) 

    class Meta:
        model = BorrowedBook
        fields = ['id', 'book', 'borrowed_on', 'return_date','number_of_days']
        
        
class UserBorrowedBookSerializer(serializers.ModelSerializer):
    borrowed_books = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id','email', 'first_name', 'last_name', 'borrowed_books']
        
    def get_borrowed_books(self, obj):
        # Filter the borrowed_books to only include those that haven't been returned
        borrowed_books = obj.borrowed_books.filter(is_returned=False)
        return BorrowedBookSerializer(borrowed_books, many=True).data