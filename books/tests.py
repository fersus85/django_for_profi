from django.test import TestCase
from django.urls import reverse
from .models import Book, Review
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


# Create your tests here
class BookTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test1', email='test1@m.com', password='123')
        self.special_permission = Permission.objects.get(codename='special_status')
        self.book = Book.objects.create(title='Test1', author='testauthor', price='25.00')
        self.review = Review.objects.create(book=self.book, author=self.user, review='good review')

    def test_book_list(self):
        self.assertEqual(f'{self.book.title}', 'Test1')
        self.assertEqual(f'{self.book.author}', 'testauthor')
        self.assertEqual(f'{self.book.price}', '25.00')

    def test_book_list_view_for_login(self):
        self.client.login(email='test1@m.com', password='123')
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test1')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_list_view_for_logout(self):
        self.client.logout()
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response, )

    def test_book_detail_view(self):
        self.client.login(email='test1@m.com', password='123')
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test1')
        self.assertContains(response, 'good review')
        self.assertTemplateUsed(response, 'books/book_detail.html')
