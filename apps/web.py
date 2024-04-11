from flask import Flask, request, jsonify, render_template
from prometheus_client import Counter, Summary, generate_latest
import os
import psycopg

from components.database import get_arxiv_latest, get_arxiv_after
from models.article import Article

index_view_metric = Counter('index', 'GET index')
index_duration = Summary('index_duration', 'GET index duration')
api_latest_metric = Counter('latest', 'GET /api/latest')
api_latest_duration = Summary('latest_duration', 'GET /api/latest duration')
api_after_metric = Counter('after', 'GET /api/after')
api_after_duration = Summary('after_duration', 'GET /api/after duration')

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

    @app.route("/api/latest", methods=["GET"])
    @api_latest_duration.time()
    def latest():
        api_latest_metric.inc()

        with psycopg.connect(database_url) as conn:
            with conn.cursor() as cur:
                arxiv = get_arxiv_latest(cur)
        articles = list(map(lambda a: a.to_article(audio_url_root), arxiv))

        return jsonify(articles)

    @app.route("/api/after", methods=["POST"])
    @api_after_duration.time()
    def after():
        api_after_metric.inc()

        aid = request.json['id']

        with psycopg.connect(database_url) as conn:
            with conn.cursor() as cur:
                arxiv = get_arxiv_after(cur, aid)
        articles = list(map(lambda a: a.to_article(audio_url_root), arxiv))

        return jsonify(articles)

    @app.route("/healthz")
    def healthz():
        return 'ok'
    @app.route("/metrics")
    def metrics():
        return generate_latest()

    return app
