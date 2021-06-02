import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("FLASK_ENV", default='production')
DEBUG = ENV == "development"
SECRET_KEY = os.getenv('SECRET_KEY', default='octocat')
SCHEDULER_API_ENABLED = os.getenv("SCHEDULER_API_ENABLED", default=True)