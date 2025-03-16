from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from django_filters import rest_framework
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAuthenticated

# Create your views here.

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveAPIView):
    serializer_class = BookSerializer

    def get_object(self):
        book = Book.objects.get(pk=self.kwargs['pk'])
        return book

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer