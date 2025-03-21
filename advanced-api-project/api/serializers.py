from rest_framework import serializers
from .models import Book, Author
import datetime

class BookSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Book
        fields = ('title', 'publication_year', 'author')

    def validate_publication_year(self,value):
        today = datetime.date.today()
        year = today.year
        pub_year = int(value)
        if pub_year == year:
            raise serializers.ValidationError(f"The year of publication must be on or before {year}")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('name')