from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from .views import BookList, BookViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),  # Maps to the BookList view
    path('', include(router.urls)), # Maps to the BookViewSet view
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'), # Maps to the obtain_auth_token view
]

