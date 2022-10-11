# Simple API with FastAPI

Construction of an API for full user CRUD including manipulation of profile images. In this project, FastAPI, SQLAlchemy, SQLModel, Postgres, Alembic, and Docker were used.

## Project initialization by DOCKER

Building the project:
```
$ docker-compose build
```

Initializing the project:
```
$ docker-compose up
```

## API usage examples

### API Doc:
To access the API documentation, access the address:: [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)

### Add a user:

```sh
$ curl -d '{"name":"Thiago Cruz", "email":"thiagoaugustocruz@gmail.com"}' -H "Content-Type: application/json" -X POST http://0.0.0.0:8000/users
```

### Get all users:
Use the route: [http://0.0.0.0:8000/users](http://0.0.0.0:8000/users)
