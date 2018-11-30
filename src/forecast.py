from forecastio import load_forecast
from src.key import D_SECRET_KEY
from data.places import places
import pickle
import random


def _read_from_file():
    fh = open('C:/Users/User/Documents/Ulster/TwitterProject/data/random.pkl', 'rb')
    posted = pickle.load(fh)
    fh.close
    return posted


def _write_to_file(posted):
    fh = open('C:/Users/User/Documents/Ulster/TwitterProject/data/random.pkl', 'wb')
    pickle.dump(posted, fh)
    fh.close()


class Forecast:

    def __init__(self, place):
        if place == "None":
            self._return_random_place()
        elif place.isalpha():
            self.__place = place
        else:
            raise ValueError('Only alphabetical characters accepted')
        self.__forecast = load_forecast(D_SECRET_KEY, *places[self.__place])

    def get_current_summary(self):
        now_summary = self.__forecast.currently().summary
        return now_summary

    def get_weekly_summary(self):
        weekly_summary = self.__forecast.daily().summary
        return weekly_summary

    def get_current_temperature(self):
        now_temperature = str(round(self.__forecast.currently().temperature))
        now_temperature += "°"
        return now_temperature

    def get_place_name(self):
        return self.__place

    # def weekly_temperature_low(self):
    #     min_temperature = str(self.forecast.daily().data("temperatureLow"))
    #     min_temperature += "°"
    #     return min_temperature
    #
    # def weekly_temperature_high(self):
    #     max_temperature = str(self.forecast.daily().data("temperatureHigh"))
    #     max_temperature += "°"
    #     return max_temperature

    def format_current_summary(self):
        return "Current weather for {}:\n{} with a temperature of {}\n".format(self.get_place_name(),
                                                                             self.get_current_summary(),
                                                                             self.get_current_temperature())

    def format_weekly_summary(self):
        return "Weekly weather for {}: \n{}\n".format(self.__place, self.get_weekly_summary())
        # print("In daytime, a temperature high of {} and a low of {}".format(self.weekly_temperature_high(),
        #                                                                     self.weekly_temperature_low()))

    # Returns a randomly chosen place that is not already randomly chosen, until all places have been chosen
    def _return_random_place(self):
        posted_random_forecast = _read_from_file()
        if len(posted_random_forecast) == len(places):

            del posted_random_forecast[:]

        choice = random.choice(list(places))
        while choice in posted_random_forecast:
            choice = random.choice(list(places))

        posted_random_forecast.append(choice)

        _write_to_file(posted_random_forecast)
        self.__place = choice
        return self.__place


# random_forecast = Forecast("None")
#
# print(random_forecast.get_place_name())
# print(random_forecast.format_current_summary())
#
# print(random_forecast.format_weekly_summary())
#
#
# print(len(places))
#
# print(len(_read_from_file()))
