from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from model_bakery import baker
from .models import User, Book, BorrowedBook
from datetime import timedelta
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from .signals import publish_user_changes, publish_borrowed_book_changes


class UserCreateViewTest(APITestCase):
    def setUp(self):
        post_save.disconnect(publish_user_changes, sender=User)
        post_save.disconnect(publish_borrowed_book_changes, sender=BorrowedBook)
        self.user_data = {'email': 'test@example.com', 'first_name': 'Test', 'last_name': 'User'}
        self.url = reverse('list_createa_user')


    def test_create_user(self):
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, 'test@example.com')

class BookListViewTest(APITestCase):
    def setUp(self):
        post_save.disconnect(publish_user_changes, sender=User)
        post_save.disconnect(publish_borrowed_book_changes, sender=BorrowedBook)
        self.book = baker.make(Book, publisher='Test Publisher', category='Science', available=True)
        self.url = reverse('book_list')
        

    def test_list_books(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class BookRetrieveViewTest(APITestCase):
    def setUp(self):
        post_save.disconnect(publish_user_changes, sender=User)
        post_save.disconnect(publish_borrowed_book_changes, sender=BorrowedBook)
        self.book = baker.make(Book)
        self.url = reverse('book_retrive', kwargs={'pk': self.book.pk})


    def test_retrieve_book(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.book.pk)
        

class BorrowBookViewTest(APITestCase):
    def setUp(self):
        post_save.disconnect(publish_user_changes, sender=User)
        post_save.disconnect(publish_borrowed_book_changes, sender=BorrowedBook)
        self.book = baker.make(Book, available=True)
        self.user = baker.make(User)
        self.url = reverse('borrow_book')
        self.data = {
            'book_id': self.book.pk,
            'user_email': self.user.email,
            'number_of_days': 7
        }


    def test_borrow_book(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.book.refresh_from_db()
        self.assertFalse(self.book.available)

    def test_borrow_unavailable_book(self):
        # Set book to unavailable
        self.book.available = False
        self.book.save()
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

