from forecastio import load_forecast
from src.key import D_SECRET_KEY
from data.places import places
from data.posted_random_forecast import (_read_from_file,
                                         _write_to_file)
import random


class Forecast:

    def __init__(self, place):
        if place == "None":
            self._return_random_place()
        elif place.isalpha():
            self.place = place
        else:
            raise ValueError('Only alphabetical characters accepted')
        self.forecast = load_forecast(D_SECRET_KEY, *places[self.place])

    def get_current_summary(self):
        now_summary = self.forecast.currently().summary
        return now_summary

    def get_current_temperature(self):
        now_temperature = str(round(self.forecast.currently().temperature))
        now_temperature += "°"
        return now_temperature

    def get_weekly_summary(self):
        weekly_summary = self.forecast.daily().summary
        return weekly_summary

    # def weekly_temperature_low(self):
    #     min_temperature = str(self.forecast.daily().data("temperatureLow"))
    #     min_temperature += "°"
    #     return min_temperature
    #
    # def weekly_temperature_high(self):
    #     max_temperature = str(self.forecast.daily().data("temperatureHigh"))
    #     max_temperature += "°"
    #     return max_temperature

    def display_current_summary(self):
        print("Current weather for " + self.place)
        print("{} with a temperature of {}\n".format(self.get_current_summary(), self.get_current_temperature()))

    def display_weekly_summary(self):
        print("Weekly weather for {}: \n{}\n".format(self.place, self.get_weekly_summary()))
        # print("In daytime, a temperature high of {} and a low of {}".format(self.weekly_temperature_high(),
        #                                                                     self.weekly_temperature_low()))

    def get_place_name(self):
        return self.place

    # Returns a randomly chosen place that is not already randomly chosen, until all places have been chosen
    def _return_random_place(self):
        posted_random_forecast = _read_from_file()
        print(posted_random_forecast)
        if len(posted_random_forecast) == len(places):

            del posted_random_forecast[:]

        choice = random.choice(list(places))
        while choice in posted_random_forecast:
            choice = random.choice(list(places))

        posted_random_forecast.append(choice)

        _write_to_file(posted_random_forecast)
        self.place = choice
        return self.place


random_forecast = Forecast("None")

print(random_forecast.get_place_name())
random_forecast.display_current_summary()

random_forecast.display_weekly_summary()


print(len(places))


