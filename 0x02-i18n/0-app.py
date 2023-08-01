#!/usr/bin/env python3
"""simple flask module"""
from flask import Flask, render_template
from typing import Any


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index() -> Any:
    """renders home page"""
    return render_template('0-index.html')


if __name__ == '__main__':
    app.run(debug=True)
