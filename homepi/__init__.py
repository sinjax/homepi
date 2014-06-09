
import logging
from flask import Flask
from IPython import embed
app = Flask(__name__.split('.')[0])
app.config.from_object('homepi.envvar')



import views
import admin