**Books Api** is a simple app created in Django Rest Framework, that is based on [Google book api](https://www.googleapis.com/books/v1/volumes). App allows to get books from api based on user's query and save results to the database.

## Local usage

### Requirements

Docker and Docker-Compose are requied to run this app.

To use app locally user need first to create an `.env` file with below keys:
```
SECRET_KEY = <django secret key>
ALLOWED_HOSTS = <localhost or other host name>
POSTGRES_NAME = <postgres database name>
POSTGRES_USER = <postgres user name>
POSTGRES_PASSWORD = <postgres user password>
POSTGRES_HOST = <postgres host>
POSTGRES_PORT = <postgres port>
```

To run this aplication use bellow commands:

```docker
docker-compose build
docker-compose up
docker-compose run web python3 manage.py makemigrations main_api
docker-compose run web python3 manage.py migrate main_api
docker-compose run web python3 manage.py migrate
```

## Heroku usage

Application is fully hosted on [Heroku](https://books-api-mw.herokuapp.com/), there is no need to do anything more.

## Endpoints

`/db` - POST endpoint for making querry to the google api, requires `q` parameter.

`/books` - GET endpoint for reading all books saved in the database by previous queries

`/books/<id>` - GET endpoint for book detail by its id