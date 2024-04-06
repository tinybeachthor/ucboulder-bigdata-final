# arXiv podcast - UCBoulder big data final project

Audio arXiv - papers as a podcast

## Overview

1. Pull new computer science papers from arXiv
2. Run text2speech using bark on them
3. Present as a website with the option to play the audio

## Setup

### Setup python environment

Create python `venv`. Install runtime dependencies. Install test
dependencies.

```sh
python -m venv venv
pip install -r requirements.txt
pip install pytest
```

### Setup development infrastructure

Spin up the dockerized infrastructure. Setup database tables using `flyway`.

```sh
docker compose up
make setup
```

### Run the app

Run the data collector. This is a job that will pull the latest articles
from arxiv API and push them to a work queue, then exit.

```sh
python main.py collect
```

Run the data processor worker. Get item from work queue, run text2speech,
push the audio to object storage, insert article info to database.

```sh
python main.py process
```

Run the web app + API server.

```sh
flask --app main.py run
```
