#!/usr/bin/env python
"""Flacon example."""

import argparse

import flask
from flacon import Flacon

# Optional API.
try:
    import flask_restx
except ImportError:
    flask_restx = None


class Error(Exception):

    """All local errors."""

    pass


# This could be as simple as :
# flacon = Flacon(app)
# app = flacon.app

# More complicated example:

flacon = Flacon(__name__)
app = flacon.app


# Override the default index


@app.route("/")
def index():
    return flask.render_template("index.html")


# Add a new page.


@app.route("/example")
def example():
    return flask.render_template("example.html")


# Create a custom health check callbback.


def is_healthy():
    """Custom "health" check."""
    import random

    if random.random() > 0.5:
        raise Error()

    return True


if flask_restx:

    class HelloWorld(flask_restx.Resource):
        def get(self):
            return {"hello": "world"}


def initialize_api(flask_app):
    """Initialize an API."""
    if not flask_restx:
        return

    api = flask_restx.Api(version="1.0", title="My Example API")
    api.add_resource(HelloWorld, "/hello")

    blueprint = flask.Blueprint("api", __name__, url_prefix="/api")
    api.init_app(blueprint)
    flask_app.register_blueprint(blueprint)


def initialize_app(flask_app, args):
    """Initialize the App."""
    # Setup flacon with the args.
    flacon.setup(args)

    # Register a custom health check.
    flacon.is_healthy = is_healthy

    # Add an optional API
    initialize_api(flask_app)


def main():
    # Setup a custom parser.
    parser = argparse.ArgumentParser(description="Example")
    parser = Flacon.get_argparser(parser)
    args = parser.parse_args()

    initialize_app(app, args)

    # Start the application.
    flacon.run()


if __name__ == "__main__":
    main()
