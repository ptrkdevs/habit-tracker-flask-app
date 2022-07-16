from flask import Flask
from routes import pages
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():

    app = Flask(__name__)

    db = MongoClient(os.environ.get("MONGODB_URI"))

    app.db = db.get_default_database()

    app.register_blueprint(pages)

    return app
