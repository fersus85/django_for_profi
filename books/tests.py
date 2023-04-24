from django.test import TestCase
from django.urls import reverse
from .models import Book


# Create your tests here
class BookTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title='Test1', author='testauthor', price='25.00')

    def test_book_list(self):
        self.assertEqual(f'{self.book.title}', 'Test1')
        self.assertEqual(f'{self.book.author}', 'testauthor')
        self.assertEqual(f'{self.book.price}', '25.00')

    def test_book_list_view(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test1')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_detail_view(self):
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test1')
        self.assertTemplateUsed(response, 'books/book_detail.html')
