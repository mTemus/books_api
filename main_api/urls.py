from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main_api.views import BooksGenericViewset

router = DefaultRouter()
router.register(r'books', BooksGenericViewset, basename='books')

urlpatterns = router.urls