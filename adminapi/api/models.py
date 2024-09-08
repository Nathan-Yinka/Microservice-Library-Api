from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    available = models.BooleanField(default=True)


class User(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class BorrowedBook(models.Model):
    user = models.ForeignKey(User, related_name='borrowed_books', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_on = models.DateField(auto_now_add=True)
    number_of_days = models.IntegerField()
    return_date = models.DateField()
    is_returned = models.BooleanField(default=False)
    