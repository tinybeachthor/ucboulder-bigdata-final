# Rubric

A quick overview of where to find all the graded items.
Explanation of how all the graded items were addressed.

<!-- toc -->

## Web app

Web server handling the presentation of the data to users.
It is located in `apps/web.py`.
It is implemented using `flask` web framework and in production served
through `gunicorn`.

## Data collection

The job collecting new data. Located in `apps/collect.py`. It is invoked
every hour using the `heroku scheduler`.

## Data analyzer

The worker processing collected data. The main part is running text to
speech and storing data and audio in database and object storage,
respectively. The code is in `apps/process.py`.

## Unit tests

Unit tests are co-located with the files they test in the same
directory. For example, `components/database.py` has unit tests in
`components/database_test.py`. Unit tests are discovered and run using
`pytest`.

## Data persistence

Data about the articles is stored in a PostgreSQL database. The data is
indexed by publication date and allows retrieval ordered by the date.

The audio files are stored in an S3-like block storage, specifically
Cloudflare R2 which allows direct public access through a CDN network.

## Rest collaboration or API endpoint

The web server (`apps/web.py`) also exposes a REST API endpoint. This
API is used to handle a 'load more' request from the website to load
older articles. The API is also publicly accessible and can be used for
programmatic access to the service.

## Product environment

Production deployment in Heroku. Using `docker-compose` to create a
local development environment with all the services running locally in
docker: database, S3, rabbit queue, prometheus, grafana.

## Integration tests

Integration tests are in the `integration` directory. They are
discovered and run using `pytest`.

## Mocks or test doubles

Mocks and Spies are used extensively throughout unit tests.
For example, in `components/database_test.py` a database `MockCursor` is
created to mimic the data returned from the database. Database access
functions are then tested against this mock object.

## Continuous Integration

Using `GitHub Actions`. The configuration is in `.github/workflows/test.yml`.
All the unit and integration tests are run on every push to the
repository.

## Production monitoring

To collect application metrics (processing time, request counts, ...) we
utilize prometheus metrics and expose them on the `/metrics` endpoint.

For system metrics (CPU usage, RAM use, restarts, ...), we utilize the
built in Heroku monitoring dashboard.

## Event collaboration messaging

The `collect` job places new articles found into a rabbit message queue.
The `process` worker is pulling items from this queue and handling them.
This way we can easily scale up the number of workers as needed.

## Continuous Delivery

Using `Heroku <-> GitHub` integration. After every new push, if
continuous integration passes, a new deployment is created.

