
import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123123123123123'
    SQLALCHEMY_DATABASE_URI="postgresql://postgres:STRONGPASSWORD@localhost/testdb"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    