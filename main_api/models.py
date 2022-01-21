from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField("Author")
    published_date = models.PositiveSmallIntegerField(
        default=1000,
        validators=[
            MaxValueValidator(2020),
            MinValueValidator(1000)
        ]
    )
    categories = models.ManyToManyField("Category")
    average_rating = models.PositiveSmallIntegerField(default=0)
    ratings_count = models.PositiveSmallIntegerField(default=0)

    def __str__(self) -> str:
        return self.title

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
