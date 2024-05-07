import os

from flask import Flask

def create_app(test_config=None):
    app = flask.Flask(__name__, instance_relative_config=True)