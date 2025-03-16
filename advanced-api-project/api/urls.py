from django.urls import path
from .views import BookListView, BookDetailView, BookCreateView
from .views import BookDeleteView, BookUpdateView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-get'),
    path('books/add/', BookCreateView.as_view(), name='add-book'),
]