
from os import environ, path
basedir = path.abspath(path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv(path.join(basedir, '.env'))

class Config(object):
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') or \
        'sqlite:///' + path.join(basedir, 'Database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = environ.get('SECRET_KEY') or 'you-will-never-guess'
    #new
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    UPLOAD_FOLDER = 'app/uploads'