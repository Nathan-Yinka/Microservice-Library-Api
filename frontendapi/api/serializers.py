# serializers.py
from rest_framework import serializers
from .models import Book, User,BorrowedBook
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
    def validate_email(self, value):
        """
        Validate the email address for format and uniqueness.
        """
        value = value.lower()
        try:
            validate_email(value)
        except ValidationError as e:
            raise serializers.ValidationError("Invalid email format.") from e
        
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        
        return value

    def validate(self, data):
        """
        Perform any additional validations that require checking multiple fields.
        """
        
        data = super().validate(data)
        first_name = data['first_name'].strip().title()
        last_name = data['last_name'].strip().title()
        
        data['last_name'] = last_name
        data['first_name'] = first_name
        
        return data
        

class BorrowBookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    user_email = serializers.EmailField()
    number_of_days = serializers.IntegerField()
    
    def validate_email(self, value):
        """
        Validate the email address for format and uniqueness.
        """
        value = value.lower()
        try:
            validate_email(value)
        except ValidationError as e:
            raise serializers.ValidationError("Invalid email format.") from e
        
        
        return value
    


class BorrowedBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True) 

    class Meta:
        model = BorrowedBook
        fields = ['id', 'book', 'borrowed_on', 'return_date', 'number_of_days','user']
        
        
class UserBorrowedBookSerializer(serializers.ModelSerializer):
    borrowed_books = BorrowedBookSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id','email', 'first_name', 'last_name', 'borrowed_books']