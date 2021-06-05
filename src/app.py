import os
from flask import Flask
from src import settings
from src.extensions import api, api_bp
from src.resources.image import Image
from src.resources.todo import Todo

project_directory = os.path.dirname(os.path.abspath(__file__))


def create_app(config_object=settings):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)


    create_api_resources()
    register_blueprints(app)

    return app

def register_blueprints(app):
    app.register_blueprint(api_bp)

def create_api_resources():
    api.add_resource(Image, "/images")
    api.add_resource(Todo, "/todo", "/todo/<int:note_id>")
