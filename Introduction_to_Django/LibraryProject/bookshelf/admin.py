from django.contrib import admin


# Register your models here.
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pulication_year')
    list_filter = ('author', 'pulication_year')
    search_fields = ('title', 'author', 'pulication_year')

admin.site.register(Book, BookAdmin)