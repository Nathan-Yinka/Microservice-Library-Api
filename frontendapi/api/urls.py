from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.UserCreateView.as_view(), name="list_createa_user"),
    path("books/", views.BookListView.as_view(), name="book_list"),
    path("books/<int:pk>/", views.BookRetrieveView.as_view(), name="book_retrive"),
    path("borrow_book/", views.BorrowBookView.as_view(), name="borrow_book")
]
