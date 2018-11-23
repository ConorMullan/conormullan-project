from forecastio import load_forecast
from src.key import D_SECRET_KEY
import datetime

boston = load_forecast(D_SECRET_KEY, 42.3601, -71.0589)

byHour = boston.hourly()

print(byHour.summary)