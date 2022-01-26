from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=1000)
    authors = models.ManyToManyField(Author, through='BookAuthor')
    published_date = models.PositiveSmallIntegerField(
        default=1000,
        validators=[
            MaxValueValidator(2022),
            MinValueValidator(1000)
        ]
    )
    categories = models.ManyToManyField(Category, through='BookCategory')
    average_rating = models.PositiveSmallIntegerField(default=0)
    ratings_count = models.PositiveSmallIntegerField(default=0)
    thumbnail = models.CharField(max_length=300, default="")

class BookAuthor(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

class BookCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title