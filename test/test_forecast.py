import forecastio as fc
from src.forecast import *
from .config import *
import unittest
import random
from mock import Mock, patch


class TestForecast(unittest.TestCase):

    def setUp(self):
        self.forecast = Forecast("Dungiven")

    @patch.object(fc.load_forecast, 'currently')
    def test_get_current_summary(self):
        expected = pass
        result = self.mock_forecast.currently().summary
        return now_summary

    @patch.object(fc.load_forecast, 'daily')
    def test_get_weekly_summary(self):
        expected =
        result= self.mock_forecast.daily().summary
        return weekly_summary

    @patch.object(fc.load_forecast, 'currently')
    def test_get_current_temperature(self):
        result = str(round(self.mock_forecast.currently().temperature))

        return now_temperature

    def test_get_place_name(self):
        expected
        return self.mock_forecast.__place_name

    def test_get_alert(self):
        alert = self.__forecast.alerts()
        return alert