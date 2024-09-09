# tests.py
from django.urls import reverse
from django.db.models.signals import post_save, post_delete
from rest_framework.test import APITestCase
from rest_framework import status
from model_bakery import baker
from .models import Book, User, BorrowedBook
from .signals import handle_book_save, handle_book_delete

class BookAPITest(APITestCase):
    def setUp(self):
        post_save.disconnect(handle_book_save, sender=Book)
        post_delete.disconnect(handle_book_delete, sender=Book)
        self.book = baker.make(Book)
        self.book_list_create_url = reverse('book_list_create')
        self.book_detail_url = reverse('book_update_retrieve_delete', kwargs={'pk': self.book.pk})


    def test_list_books(self):
        response = self.client.get(self.book_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_create_book(self):
        data = {'title': 'New Book', 'publisher': 'New Publisher', 'category': 'New Category', 'available': True}
        response = self.client.post(self.book_list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_retrieve_book(self):
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    def test_update_book(self):
        data = {'title': 'Updated Title'}
        response = self.client.patch(self.book_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')

    def test_delete_book(self):
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

class UserAPITest(APITestCase):
    def setUp(self):
        post_save.disconnect(handle_book_save, sender=Book)
        post_delete.disconnect(handle_book_delete, sender=Book)
        self.user = baker.make(User)
        self.user_list_url = reverse('user_list')


    def test_list_users(self):
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class UserBorrowedBookAPITest(APITestCase):
    def setUp(self):
        post_save.disconnect(handle_book_save, sender=Book)
        post_delete.disconnect(handle_book_delete, sender=Book)
        self.user = baker.make(User)
        self.borrowed_books = baker.make(BorrowedBook, user=self.user)
        self.user_borrowed_books_url = reverse('user_borrowed_books')


    def test_user_borrowed_books(self):
        response = self.client.get(self.user_borrowed_books_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 

class BorrowedBookListAPITest(APITestCase):
    def setUp(self):
        post_save.disconnect(handle_book_save, sender=Book)
        post_delete.disconnect(handle_book_delete, sender=Book)
        baker.make(BorrowedBook, is_returned=False)
        self.borrowed_book_list_url = reverse('borrowed_book_list')


    def test_list_borrowed_books(self):
        response = self.client.get(self.borrowed_book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


