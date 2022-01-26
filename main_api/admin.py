from django.contrib import admin
from main_api.models import Book, Author, Category, BookAuthor, BookCategory

# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(BookAuthor)
admin.site.register(BookCategory)