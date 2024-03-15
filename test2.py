# API fournie ici doit obtenir la qualité de l'air par longitude et latitude.
# Nous pouvons utiliser le nom de la ville pour obtenir la longitude et la 
# latitude de l'API précédente, puis l'appliquer à cette API.
import requests
from datetime import datetime, timedelta
import csv

api_key = 'c96bb98a69fc64d39530c5d0ddef3f8a'
city_name = 'Paris'
#  DATE UN MOIS
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()
# print(end_date)
# https://openweathermap.org/current
# api--->https://pro.openweathermap.org/data/2.5/forecast/climate?q=London&appid={API key}
url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
#res
weather_response = requests.get(url)
weather_data = weather_response.json()

print(weather_data)
# "coord": {
#    "lon": 10.99,
#    "lat": 44.34
#  }
lat = weather_data['coord']['lat']
lon = weather_data['coord']['lon']
air_pollution = []
#http://api.openweathermap.org/data/2.5/air_pollution/history?lat=508&lon=50&start=1606223802&end=1606482999&appid={API key}
air_pollution_url = f'https://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={int(start_date.timestamp())}&end={int(end_date.timestamp())}&appid={api_key}'

air_pollution_response = requests.get(air_pollution_url)
air_pollution_data = air_pollution_response.json()

print(air_pollution_data)


air_pollution_records = []
for entry in air_pollution_data['list']:
    record = {
        'date': datetime.utcfromtimestamp(entry['dt']).strftime('%Y-%m-%d'),
        'AQI': entry['main']['aqi']
    }
    record.update(entry['components'])
    air_pollution_records.append(record)

csv_file = 'air_pollution_data.csv'
with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['date', 'AQI', 'co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3'])
    writer.writeheader()
    for record in air_pollution_records:
        writer.writerow(record)

for record in air_pollution_records:
    print(record)

#       "components":{
#        "co":201.94053649902344,
#        "no":0.01877197064459324,
#        "no2":0.7711350917816162,
#        "o3":68.66455078125,
#        "so2":0.6407499313354492,
#        "pm2_5":0.5,
#        "pm10":0.540438711643219,
#        "nh3":0.12369127571582794
#      }
#SO2	NO2	PM10	PM2.5	O3	CO

