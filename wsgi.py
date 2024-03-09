from flask import Flask
from flask_cors import CORS
from chatapp.api_server import chat_blueprint
from config import Config


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:8000"}})

app.register_blueprint(chat_blueprint)


if __name__ == "__main__":
    app.run(port=5000)
