# rinhadebackend-2023

Python 3.9
FastApi
SQLAlchemy
PostgreSQL

## Build Image

docker-compose build
docker-compose up -d --build
docker-compose run --service-ports --rm api1 bash
docker-compose run -e TESTING=True --rm api1 pytest

## Run Server

```sh
$ poetry run uvicorn app:main --reload
```

```sh
# Exemplos de requests
curl -v -XPOST -H "content-type: application/json" -d '{"apelido" : "xpto", "nome" : "xpto xpto", "nascimento" : "2000-01-01", "stack": null}' "http://localhost:9999/pessoas"
curl -v -XGET "http://localhost:9999/pessoas/1"
curl -v -XGET "http://localhost:9999/pessoas?t=xpto"
curl -v "http://localhost:9999/contagem-pessoas"
```

## Run Tests

```sh
$ poetry run pytest .
```

```sh
$ docker-compose run --rm api1 pytest -s -k test_routers
```
