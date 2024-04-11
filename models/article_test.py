from flask import Flask, jsonify
from .article import Article

def test_jsonify():
    authors = ["a", "aa", "aaa"]
    summary = """
    Multiline
    string
    """
    audio_url = "https://localhost:5000/___id___"
    article = Article("id", "link", "title", authors, summary, audio_url)

    app = Flask(__name__)
    with app.app_context():
        response = jsonify(article)

    assert response.status_code == 200
    assert response.status == "200 OK"
    assert response.is_json
