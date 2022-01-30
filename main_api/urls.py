from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main_api.views import BooksGenericViewset, QueryGenericViewset

router = DefaultRouter()
router.register(r'books', BooksGenericViewset, basename='books')
router.register(r'', QueryGenericViewset, basename='db')

urlpatterns = router.urls