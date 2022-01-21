from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main_api.views import BooksGenericViewset

router = DefaultRouter()
router.register('', BooksGenericViewset, basename='books')

urlpatterns = [
    path('books/', include(router.urls)),
]
