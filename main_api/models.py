from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField("Author")
    published_date = models.IntegerField()
    categories = models.ManyToManyField("Category")
    average_raging = models.IntegerField()
    ratings_count = models.IntegerField()

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
