#!/usr/bin/python3
'create an instace of blueprint'
from flask import Blueprint
app_views = Blueprint("my_blueprint", __name__, url_prefix="/api/v1")
from api.v1.views.index import *
from api.v1.views import states
