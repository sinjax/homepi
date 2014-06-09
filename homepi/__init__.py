
import logging
from flask import Flask

app = Flask(__name__.split('.')[0])
app.config.from_object('homepi.envvar')



import views
import admin