# Rinha de Backend (Backend Battle) - 2023

The **Backend Battle** is a stress test competition where participants develop APIs to handle the highest load possible under strict resource constraints. APIs must expose specific endpoints for managing "person" resources.

### Rules and Instructions

The competition rules include:

1. **API Endpoints**:

   - `POST /pessoas`: Create a "person" with attributes like nickname (unique), name, birthdate, and optional skill stack.
   - `GET /pessoas/{id}`: Retrieve details of a person by ID.
   - `GET /pessoas?t={term}`: Search for people by name, nickname, or skills.
   - `GET /contagem-pessoas`: Return the total count of created people.

2. **Database Options**: PostgreSQL, MySQL, or MongoDB.

3. **Resource Constraints**: APIs must run on Docker Compose with a maximum of 1.5 CPUs and 3GB of RAM, distributed among components (e.g., API instances, database, load balancer).

4. **Testing Environment**:
   - APIs are stress-tested on AWS EC2 using [Gatling (3.10.5) ](https://gatling.io/).
   - Two API instances are deployed behind an NGINX load balancer.
   - Scoring is based on the number of successful "person" entries in the database after the stress test.

For more details about submission requirements and tournament results, refer to the [official instructions](https://github.com/zanfranceschi/rinha-de-backend)
or [official X account](https://x.com/rinhadebackend).

### My Implementation:

The project is implemented using the following stack:

- **Python**
- **FastAPI** for API development
- **SQLAlchemy** for ORM and database interactions
- **PostgreSQL** as the main database
- **Redis** for caching and other optimizations

All endpoints were thoroughly tested using **pytest** to ensure correctness and reliability.

| Container | CPU  | ACC CPU | MEMORY (GB) | ACC MEMORY |
| :-------: | :--: | :-----: | :---------: | :--------: |
|   API 1   | 0,25 |  0,25   |    0,40     |    0,40    |
|   API 2   | 0,25 |  0,50   |    0,40     |    0,08    |
|   PROXY   | 0,25 |  0,75   |    0,40     |    1,20    |
| DATABASE  | 0,75 |  1,50   |    1,50     |    2,70    |
|   CACHE   | 0,10 |  1,60   |    0,50     |    3,20    |

#### Build Image

```sh
$ docker compose build
```

#### Run Tests

```sh
$ docker compose run --rm -e TESTING=True --rm api1 pytest
```

#### Execute Stress Test

```sh
$ docker compose up -d --build
```

#### Check Gatling output

```sh
$ docker compose logs -t gatling
```
