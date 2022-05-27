from distutils.log import debug
import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI="postgresql://postgres:STRONGPASSWORD@localhost/testdb"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    debug=True
    