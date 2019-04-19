import forecastio as fc
from src.forecast import *
import src
from .config import *
import unittest
import random
from mock import Mock, patch


class TestForecast(unittest.TestCase):

    def setUp(self):
        self.forecast = Forecast("dungiven")

    def test_get_current_summary(self):
        expected = "Partly Cloudy"
        result = self.forecast.get_current_summary()
        self.assertEqual(expected, result)

    def test_get_weekly_summary(self):
        expected = "Light rain on Thursday, with high temperatures falling to 14°C next Friday."
        result = self.forecast.get_weekly_summary()
        self.assertEqual(expected, result)

    def test_get_place_name(self):
        expected = "dungiven"
        result = self.forecast.get_place_name()

    def test_format_weekly_summary(self):
        expected = "Weekly weather for Dungiven: \n\nLight rain on Thursday, with high temperatures falling to 14°C " \
                   "next Friday.\n"
        result = self.forecast.format_weekly_summary()
        self.assertEqual(expected, result)

    def test_format_current_summary(self):
        expected = "Current weather for Dungiven:\n\nPartly Cloudy with a temperature of 8°\n"
        result = self.forecast.format_current_summary()
        self.assertEqual(expected, result)

    def test_get_alert(self):
        expected = []
        result = self.forecast.get_alert()
        self.assertEqual(expected, result)
