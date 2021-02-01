import os

base = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")\
        or 'sqlite:///'+os.path.join(base, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret-key-here"
    UPLOAD_PATH = 'registration/static/profile/'
