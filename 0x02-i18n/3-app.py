#!/usr/bin/env python3
"""simple flask module"""
from flask import Flask, render_template, request
from flask_babel import Babel
from typing import Any


class Config(object):
    """class to keep track of supported languages"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale() -> Any:
    """gets default locale for app"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index() -> Any:
    """renders home page"""
    return render_template('0-index.html')


if __name__ == '__main__':
    app.run(debug=True)
