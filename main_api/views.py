import requests, json
from django.http import HttpResponse
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from main_api.serializers import BookSerializer, QuerySerializer
from main_api.models import Book, Author, Category, BookAuthor, BookCategory

# Create your views here.

class BooksGenericViewset(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    @action(methods=['post'], detail=False, url_path='db', url_name='db', serializer_class=QuerySerializer)
    def get_query(self, request):
        query = request.data
        serializer = QuerySerializer(data=query)
        if not serializer.is_valid():
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        
        r = requests.get('https://www.googleapis.com/books/v1/volumes', params=query)
        
        query_json = r.json()
        response_books = query_json.get("items")
        
        authors = []
        categories = []
        books = []

        books_data = self.extract_book_data(response_books)
        
        for book_data in books_data:
            authors += [Author(name=author_name) for author_name in book_data.get("authors")]
            categories += [Category(name=category_name) for category_name in book_data.get("categories")]
            
            b = [Book(
                title = book_data.get("title"),
                published_date = book_data.get("published_date"),
                average_rating = book_data.get("average_rating"),
                ratings_count = book_data.get("ratings_count"),
                thumbnail = book_data.get("thumbnail"),
            )]
            
            books += b
            print(type(b[0]), b[0], b[0].published_date)

        Author.objects.bulk_create(authors, ignore_conflicts=True)
        Category.objects.bulk_create(categories, ignore_conflicts=True)
        Book.objects.bulk_create(books, ignore_conflicts=True)
        
        authorrr = Author.objects.get(id=1)
        boook = Book.objects.all()

        ba = BookAuthor.objects.create(author=authorrr, book=boook[0])
        ba.save()

        # items > 
        #   volumeInfo >
        #       authors >
        #       publishedDate 
        #       cathegories >
        #       imageLinks >
        #           thumbnail

        return HttpResponse(status=status.HTTP_200_OK)
        
    def extract_book_data(self, response_books):
        return [{
                "title": book_data["volumeInfo"].get("title"),
                "authors": book_data["volumeInfo"].get("authors", ["UNKOWN"]),
                "published_date": book_data["volumeInfo"].get("publishedDate"),
                "categories": book_data["volumeInfo"].get("categories", ["UNKOWN"]),
                "average_rating": book_data["volumeInfo"].get("averageRating", 0),
                "ratings_count": book_data["volumeInfo"].get("ratingCount", 0),
                "thumbnail": book_data["volumeInfo"].get("imageLinks", {}).get("thumbnail"),
            } for book_data in response_books]
        


# - bulk_create książek 
# - bulk_create autorów
# - bulk_create kategorii 
# - wyciągnięcie z bazy książek 
# - wyciągnięcie z bazy autorów 
# - wyciągnięcie z bazy kategorii 
# pogrupowanie ich 
# - bulk create relacji książki-autorzy 
# - bulk_create relacji książki-kategorie