# arXiv podcast - UCBoulder big data final project

Audio arXiv - papers as a podcast

## Overview

1. Pull new computer science papers from arXiv
2. Run text2speech using bark on them
3. Present as a website with the option to play the audio

## Setup

1. Create python virtual env: `python -m venv venv`
2. Install dependencies: `pip install -r requirements.txt`
3. Setup infrastructure: `docker-compose up`
4. Setup databases: `make setup`
5. Run data processor: `python main.py process`
6. Run data collector: `python main.py collect`
7. Start the webapp: `flask --app main.py run`
