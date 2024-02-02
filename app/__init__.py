__author__ = 'Taras Dubrava'
__date__ = 'January 2024'
__copyright__ = '(C) 2024, Taras Dubrava'

# imports
from flask import Flask
from app.config import Config

app = Flask(__name__, template_folder='webstaff', static_folder='webstaff')
app.config.from_object(Config)

from app import routes