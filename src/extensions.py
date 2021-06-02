from flask import Blueprint
from flask_restful import Api
from flask_apscheduler import APScheduler

api_bp = Blueprint("api", __name__)
api = Api(api_bp)

scheduler = APScheduler()