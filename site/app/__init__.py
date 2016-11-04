# coding: utf-8
"""
    __init__.py
    ```````````

    init file for railgun-site,
"""

from flask import Flask
from flask_flatpages import FlatPages
from config import config


app = Flask(__name__)
app.config.from_object(config['default'])
pages = FlatPages(app)


from . import views
