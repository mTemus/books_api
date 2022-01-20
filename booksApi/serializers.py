from dataclasses import fields
from rest_framework import serializers
from main_api.models import Book, Author, Category

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class CathegorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'