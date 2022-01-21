from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from main_api.serializers import BookSerializer
from main_api.models import Book

# Create your views here.

class BooksGenericViewset(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def create(self, request, *args, **kwargs):
        pass
