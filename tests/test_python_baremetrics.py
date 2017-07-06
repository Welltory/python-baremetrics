#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `python_baremetrics` package."""

import unittest

from python_baremetrics import BaremetricsClient

TEST_TOKEN = 'sk_u8fHvBAO4ubaMrlMSQfNlg'


class TestPython_baremetrics(unittest.TestCase):
    """Tests for `python_baremetrics` package."""

    def setUp(self):
        self.test_client = BaremetricsClient(token=TEST_TOKEN, sandbox=True)

    def tearDown(self):
        del self.test_client

    def test_000_something(self):
        test_account = self.test_client.get_account()
        self.assertIsNotNone(test_account)

    def test_001_list_sources(self):
        test_sources = self.test_client.list_sources()
        self.assertIsNotNone(test_sources)

    def test_002_list_plans(self):
        test_sources = self.test_client.list_sources().get('sources')
        test_plans = self.test_client.list_plans(test_sources[0]['id'])
        self.assertIsNotNone(test_plans)
