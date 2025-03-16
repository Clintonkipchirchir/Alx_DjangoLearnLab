# remove them
# api/test_views.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book, Author

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create an Author instance for tests.
        self.author = Author.objects.create(name="John Doe", bio="A sample author bio")
        
        # Create a Book instance for initial tests.
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            published_date="2021-01-01"
        )
        
        # Set up endpoint URLs.
        self.book_list_url = reverse('book-list')
        # If you have a detail endpoint, ensure your urls.py includes a name like 'book-detail'
        self.book_detail_url = reverse('book-detail', kwargs={'pk': self.book.id})
        
        # Create a user for authentication tests.
        self.user = User.objects.create_user(username='testuser', password='password')
    
    def test_get_books(self):
        """Test retrieving a list of books."""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        titles = [book["title"] for book in response.data]
        self.assertIn("Test Book", titles)
    
    def test_create_book(self):
        """Test creating a new book entry."""
        data = {
            "title": "New Book",
            "author": self.author.id,  # Use the primary key if serializer expects it
            "published_date": "2022-05-15"
        }
        response = self.client.post(self.book_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Book")
    
    def test_update_book(self):
        """Test updating an existing book."""
        data = {"title": "Updated Test Book"}
        response = self.client.patch(self.book_detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Test Book")
    
    def test_delete_book(self):
        """Test deleting a book."""
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())
    
    def test_permissions(self):
        """Test that authentication/permissions work as expected."""
        # Log out to simulate an unauthorized request.
        self.client.logout()
        data = {
            "title": "Unauthorized Book",
            "author": self.author.id,
            "published_date": "2022-06-01"
        }
        response = self.client.post(self.book_list_url, data, format="json")
        # Expect a 401 (Unauthorized) or 403 (Forbidden) if endpoint is protected.
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
    
    def test_filtering_searching_ordering(self):
        """Test filtering, searching, or ordering functionality if applicable."""
        # Example: Testing a search by title if your API supports it.
        response = self.client.get(self.book_list_url, {"search": "Test Book"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
