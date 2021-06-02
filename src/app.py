import os
import shutil
import logging
from flask import Flask, jsonify
from src import settings
from src.extensions import api, api_bp, scheduler
from src.resources.image import Image
from src.resources.todo import Todo

project_directory = os.path.dirname(os.path.abspath(__file__))


def create_app(config_object=settings):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    register_extensions(app)
    create_api_resources()
    register_blueprints(app)
    create_temp_directories()

    return app

def register_extensions(app):
    scheduler.init_app(app)
    logging.getLogger("apscheduler").setLevel(logging.INFO)
    with app.app_context():
        from src.utilities import schedules
        scheduler.start()
        from src.utilities import events

def register_blueprints(app):
    app.register_blueprint(api_bp)

def create_temp_directories():
    image_path = os.getenv("IMAGE_FILE_PATH")

    if os.path.exists(image_path):
        shutil.rmtree(image_path)
        os.makedirs(image_path)
    else:
        os.makedirs(image_path)


def create_api_resources():
    api.add_resource(Image, "/images")
    api.add_resource(Todo, "/todo", "/todo/<int:note_id>")
