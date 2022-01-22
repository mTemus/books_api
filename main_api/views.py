from django.http import HttpResponse
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from main_api.serializers import BookSerializer, QuerySerializer
from main_api.models import Book

# Create your views here.

class BooksGenericViewset(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    
    def get_serializer_class(self):
            if self.action == "post":
                return QuerySerializer
            return self.serializer_class

    @action(methods=['post'], detail=False, url_path='db', url_name='db')
    def get_query(self, request):
        user_query = request.data

        if not user_query:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        else:
            print(user_query)
            return HttpResponse("Test POST response.")

        

# bulk_create  i bulk_update

# 1. łączyło się z api googlowym i pobierało z niego np 10 książek zadanych przez parametr q 
# 2. pobawić się, żeby z syfu pobranego z google wyłuskać 10 książek w wersji lubianej przez Twoją bazę 
# 3. zrobić bulk_update żeby zaktualizować książki w Twojej bazie o nowopobrane książki 
# 4. zrobić bulk_create żeby dodać książki których jeszcze w Twojej bazie nie było 
# 5. zwrócić jakąś odpowiedź, najlepiej listę tych 10ciu książek
