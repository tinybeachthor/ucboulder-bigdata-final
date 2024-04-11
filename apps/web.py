from flask import Flask, request, render_template
from prometheus_client import Counter, Summary, generate_latest
import os
import psycopg

from components.database import get_arxiv_latest
from models.article import Article

index_view_metric = Counter('index', 'GET index')
index_duration = Summary('index_duration', 'GET index duration')

def create_app():
    database_url = os.environ.get(
        'DATABASE_URL', 'postgresql://guest:guest@localhost:5432/content')
    audio_url_root = os.environ.get(
        'AUDIO_URL_ROOT', 'http://localhost:4566/objects/')

    app = Flask(__name__, root_path=os.getcwd())

    @app.route("/")
    @index_duration.time()
    def index():
        index_view_metric.inc()

        with psycopg.connect(database_url) as conn:
            with conn.cursor() as cur:
                arxiv = get_arxiv_latest(cur)
        articles = list(map(lambda a: a.to_article(audio_url_root), arxiv))

        response = render_template(
                'index.html',
                articles = articles)

        return response

    @app.route("/echo_user_input", methods=["POST"])
    def echo_input():
        input_text = request.form.get("user_input", "")
        return "You entered: " + input_text

    @app.route("/healthz")
    def healthz():
        return 'ok'
    @app.route("/metrics")
    def metrics():
        return generate_latest()

    return app
