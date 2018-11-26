from forecastio import load_forecast
from src.key import D_SECRET_KEY

from data.places import *
import random
posted = []


def choose_place():
    if len(posted) == len(places):
        del posted[:]

    choice = random.choice(list(places))
    while choice in posted:
        choice = random.choice(list(places))
    posted.append(choice)
    return choice


class Forecast:
    def __init__(self, place, *args):
        if place.isalpha():
            self.place = place
            self.forecast = load_forecast(D_SECRET_KEY, *places[self.place])
        else:
            raise ValueError('Only alphabetical characters accepted')

    def current_summary(self):
        now_summary = self.forecast.currently().summary
        return now_summary

    def current_temperature(self):
        now_temperature = str(round(self.forecast.currently().temperature))
        now_temperature += "°"
        return now_temperature

    def weekly_summary(self):
        weekly_summary = self.forecast.daily().summary
        return weekly_summary

    def weekly_temperature_low(self):
        min_temperature = str(self.forecast.daily["temperatureLow"])
        min_temperature += "°"
        return min_temperature

    def weekly_temperature_high(self):
        max_temperature = str(self.forecast.daily().data.__getattribute__("temperatureHigh"))
        max_temperature += "°"
        return max_temperature

    def display_current_summary(self):
        print("Current weather for " + self.place)
        print(self.current_summary())
        print("Temperature of " + self.current_temperature())
        print("\n")

    def display_weekly_summary(self):
        print("Weekly weather for " + self.place)
        print(self.weekly_summary())
        print("In daytime, a temperature high of {} and a low of {}".format(self.weekly_temperature_high(),
                                                                            self.weekly_temperature_low()))

    def get_place_name(self):
        return self.place


def main():
    random_forecast = Forecast(choose_place())
    print(random_forecast.get_place_name())
    random_forecast.display_current_summary()

    random_forecast.display_weekly_summary()


main()
