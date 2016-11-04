# coding: utf-8
"""
    ship::site::__init__.py
    ```````````````````````

    init file for ship-site,
        create global flask app;
        initial flask extensions.

    :LICENSE :: MIT
    :Copyright @neo1218 2016
"""

from flask import Flask
from flask_flatpages import FlatPages
from flask_frozen import Freezer
from config import config


app = Flask(__name__)
app.config.from_object(config['default'])
pages = FlatPages(app)
freezer = Freezer(app)


from . import views
