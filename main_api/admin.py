from django.contrib import admin
from main_api.models import Book, Author, Category

# Register your models here.

admin.register(Book)
admin.register(Author)
admin.register(Category)