from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.BookListCreateView.as_view(), name="book_list_create"),
    path("books/<int:pk>", views.BookRetrieveUpdateDestroyView.as_view(), name="book_update_retrieve_delete"),
    path("users/", views.UserListView.as_view(), name="user_list"),
    path("users_borrowed/", views.UserBorrowedBook.as_view(), name="user_borrowed_books"),
    path("borrowed_books/", views.BorrowedBookListView.as_view(), name="borrowed_book_list"),
]
