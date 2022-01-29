from itertools import zip_longest
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
        
        books_data = self._extract_book_data(response_books)
        books = self._create_books(books_data)
        authors = self._create_autors(books_data)
        categories = self._create_categories(books_data)

        bounded_books = self._bound_book_with_data(books_data, books, authors, categories)
        book_authors =[BookAuthor(name=book_data["book_author"], author=book_data["author"], book=book_data["book"]) for book_data in bounded_books if book_data["author"] != None]
        book_categories =[BookCategory(name=book_data["book_category"], category=book_data["category"], book=book_data["book"])  for book_data in bounded_books if book_data["category"] != None]

        [print(ba.author, ":" ,ba.book) for ba in book_authors]

        BookAuthor.objects.bulk_create(book_authors, ignore_conflicts=True)
        BookCategory.objects.bulk_create(book_categories, ignore_conflicts=True)

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def _extract_book_data(self, response_books):
        return [{
                "title": book_data["volumeInfo"].get("title"),
                "authors": book_data["volumeInfo"].get("authors", ["UNKOWN"]),
                "published_date": self._prepare_book_date(book_data["volumeInfo"].get("publishedDate")),
                "categories": book_data["volumeInfo"].get("categories", ["UNKOWN"]),
                "average_rating": book_data["volumeInfo"].get("averageRating", 0),
                "ratings_count": book_data["volumeInfo"].get("ratingCount", 0),
                "thumbnail": book_data["volumeInfo"].get("imageLinks", {}).get("thumbnail"),
            } for book_data in response_books]

    def _prepare_book_date(self, book_date):
        return book_date[:4] if book_date != None else 0

    

    def _create_book(self, book_data):
        return Book(
                title = book_data.get("title"),
                published_date = book_data.get("published_date"),
                average_rating = book_data.get("average_rating"),
                ratings_count = book_data.get("ratings_count"),
                thumbnail = book_data.get("thumbnail"),
            )

    def _get_book(self, title, collection):
        return next((book for book in collection if book.title == title), None)

    def _get_element(self, name, collection):
        return next((element for element in collection if element.name == name), None)

    def _get_list_from_book_data(self, books_data, keyword):
        return [element for book in books_data for element in book.get(keyword) if book.get(keyword)]

    def _create_books(self, books_data):
        books_names = [book.get("title") for book in books_data]
        books = [self._create_book(book) for book in books_data]
        Book.objects.bulk_create(books, ignore_conflicts=True)
        return list(Book.objects.filter(title__in=books_names))

    def _create_autors(self, books_data):
        autors_names = self._get_list_from_book_data(books_data, "authors")
        authors = [Author(name=author_name) for author_name in autors_names]
        Author.objects.bulk_create(authors, ignore_conflicts=True)
        return Author.objects.filter(name__in=autors_names)

    def _create_categories(self, books_data):
        categories_names = self._get_list_from_book_data(books_data, "categories")
        categories = [Category(name=category_name) for category_name in categories_names]
        Category.objects.bulk_create(categories, ignore_conflicts=True)
        return Category.objects.filter(name__in=categories_names)

    def _bound_book_with_data(self, books_data, books, authors, categories):
        return [{
            "book": self._get_book(book.get("title"), books),
            "author": self._get_element(author, authors),
            "category": self._get_element(category, categories),
            "book_author": author + ' - ' + book.get("title") if author != None else '',
            "book_category": book.get("title") + " { " + category + " }" if category != None else '',
            }
            for book in books_data for author, category in zip_longest(book.get("authors"), book.get("categories"))
        ]

# - bulk_create książek 
# - bulk_create autorów
# - bulk_create kategorii 
# - wyciągnięcie z bazy książek 
# - wyciągnięcie z bazy autorów 
# - wyciągnięcie z bazy kategorii 
# pogrupowanie ich 
# - bulk create relacji książki-autorzy 
# - bulk_create relacji książki-kategorie