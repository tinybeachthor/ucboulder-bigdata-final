from flask import Flask, request, render_template
import os

def create_app():
    app = Flask(__name__, root_path=os.getcwd())

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/echo_user_input", methods=["POST"])
    def echo_input():
        input_text = request.form.get("user_input", "")
        return "You entered: " + input_text

    @app.route("/healthz")
    def healthz():
        return 'ok'

    return app
