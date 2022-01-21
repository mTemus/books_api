from dataclasses import fields
from rest_framework import serializers
from main_api.models import Book, Author, Category


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["name"]

class CathegorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(read_only=True, many=True)
    categories = CathegorySerializer(read_only=True, many=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "authors",
            "published_date",
            "categories",
            "average_rating",
            "ratings_count",
        ]