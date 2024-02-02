__author__ = 'Taras Dubrava'
__date__ = 'January 2024'
__copyright__ = '(C) 2024, Taras Dubrava'

# imports
from os import environ
from os.path import abspath, dirname, join
from dotenv import load_dotenv

basedir = abspath(dirname(__file__))
load_dotenv(join(basedir, '.env'))

class Config(object):
    API_KEY = environ.get('API_KEY')
    SECRET_KEY = environ.get('SECRET_KEY')

