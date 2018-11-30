import random
from forecastio import load_forecast
from src.key import D_SECRET_KEY
from data.places import *


posted = []


class ForecastTest:

    def choose_place():
        if len(posted) == len(places):
            del posted[:]

        choice = random.choice(list(places))
        while choice in posted:
            choice = random.choice(list(places))
        posted.append(choice)
        return choice


random_place = ForecastTest.choose_place()
print(random_place)
print(places["{}".format(random_place)][0])

place = load_forecast(D_SECRET_KEY, places["{}".format(random_place)][0], places["{}".format(random_place)][1])

print("Current weather for "+random_place)
print("Temperature: "+str(place.currently().temperature)+"°\n")
print(place.currently().summary)

print(posted)
print(len(places))
print(len(posted))
