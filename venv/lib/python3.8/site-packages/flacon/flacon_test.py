"""Flacon unit tests."""

from __future__ import absolute_import

import unittest

import flask
import mockito
import prometheus_client

import flacon
from flacon import testutils


class FlaconTest(unittest.TestCase):
    def setUp(self):
        # Don't use a shared registry.
        self.registry = prometheus_client.CollectorRegistry(auto_describe=True)

    def test_basic(self):
        """Create a flacon from a name."""
        g = flacon.Flacon(__name__, registry=self.registry)
        testutils.setup(g)
        g.setup()
        self.assertIsNotNone(g)
        self.assertTrue(g.is_healthy())
        self.assertTrue(g.is_ready())
        self.assertIsNotNone(g.metrics)

    def test_flask(self):
        """Create a flacon with a flask."""
        app = flask.Flask(__name__)
        g = flacon.Flacon(app, registry=self.registry)
        testutils.setup(g)
        self.assertIsNotNone(g)

    def test_disable_embedded_logging_should_prevent_logging_from_being_configured(
        self
    ):
        logger = mockito.mock()
        app = flask.Flask(__name__)
        app.logger = logger

        g = flacon.Flacon(app, registry=self.registry)

        testutils.setup(g, ["--disable-embedded-logging"])

        mockito.verify(logger, times=0).addHandler(mockito.any())
        mockito.verify(logger, times=0).setLevel(mockito.any())

    def test_logging_should_be_enabled_by_default(self):
        logger = mockito.mock()
        app = flask.Flask(__name__)
        app.logger = logger

        g = flacon.Flacon(app, registry=self.registry)

        testutils.setup(g, [])

        mockito.verify(logger, times=1).addHandler(mockito.any())
        mockito.verify(logger, times=1).setLevel(mockito.any())
        mockito.verify(logger, times=1).info("Logging initialized.")


# TODO:
# - Test default handlers.


if __name__ == "__main__":
    unittest.main()
