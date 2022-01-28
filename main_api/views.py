import requests
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from main_api.serializers import BookSerializer, QuerySerializer
from main_api.models import Book, Author, Category, BookAuthor, BookCategory

# Create your views here.

GOOGLE_API = 'https://www.googleapis.com/books/v1/volumes'

class BooksGenericViewset(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    @action(methods=['post'], detail=False, url_path='db', url_name='db', serializer_class=QuerySerializer)
    def get_query(self, request):
        query = request.data
        serializer = QuerySerializer(data=query)
        if not serializer.is_valid():
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        
        r = requests.get(GOOGLE_API, params=query)
        
        query_json = r.json()
        response_books = query_json.get("items")
        
        authors = []
        categories = []
        books = []

        books_data = self.extract_book_data(response_books)
        
        for book_data in books_data:
            authors += [Author(name=author_name) for author_name in book_data.get("authors")]
            categories += [Category(name=category_name) for category_name in book_data.get("categories")]
            books += self.create_book(book_data)

        books_titles = list(set([book.title for book in books]))
        authors_names = list(set([author.name for author in authors]))
        category_names = list(set([category.name for category in categories]))
        
        Author.objects.bulk_create(authors, ignore_conflicts=True)
        Category.objects.bulk_create(categories, ignore_conflicts=True)
        Book.objects.bulk_create(books, ignore_conflicts=True)

        books = list(Book.objects.filter(title__in=books_titles))
        authors = list(Author.objects.filter(name__in=authors_names))
        categories = list(Category.objects.filter(name__in=category_names))
        
        book_authors = []
        book_categories = []

        for book_data in books_data:
            book = self.get_book(book_data.get("title"), books)

            for author_data in book_data.get("authors"):
                author = self.get_element(author_data, authors)
                book_authors += [BookAuthor(author=author, book=book)]

            for category_data in book_data.get("categories"):
                category = self.get_element(category_data, categories)
                book_categories += [BookCategory(category=category, book=book)]

        BookAuthor.objects.bulk_create(book_authors, ignore_conflicts=True)
        BookCategory.objects.bulk_create(book_categories, ignore_conflicts=True)
        
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
        
    def extract_book_data(self, response_books):
        return [{
                "title": book_data["volumeInfo"].get("title"),
                "authors": book_data["volumeInfo"].get("authors", ["UNKOWN"]),
                "published_date": book_data["volumeInfo"].get("publishedDate")[0:4],
                "categories": book_data["volumeInfo"].get("categories", ["UNKOWN"]),
                "average_rating": book_data["volumeInfo"].get("averageRating", 0),
                "ratings_count": book_data["volumeInfo"].get("ratingCount", 0),
                "thumbnail": book_data["volumeInfo"].get("imageLinks", {}).get("thumbnail"),
            } for book_data in response_books]
        
    def create_book(self, book_data):
        return [Book(
                title = book_data.get("title"),
                published_date = book_data.get("published_date"),
                average_rating = book_data.get("average_rating"),
                ratings_count = book_data.get("ratings_count"),
                thumbnail = book_data.get("thumbnail"),
            )]

    def get_book(self, title, collection):
        return next((book for book in collection if book.title == title), None)

    def get_element(self, name, collection):
        return next((element for element in collection if element.name == name), None)

# - bulk_create książek 
# - bulk_create autorów
# - bulk_create kategorii 
# - wyciągnięcie z bazy książek 
# - wyciągnięcie z bazy autorów 
# - wyciągnięcie z bazy kategorii 
# pogrupowanie ich 
# - bulk create relacji książki-autorzy 
# - bulk_create relacji książki-kategorie