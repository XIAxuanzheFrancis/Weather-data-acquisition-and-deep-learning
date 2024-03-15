import requests
from datetime import datetime, timedelta
import csv

api_key = 'c96bb98a69fc64d39530c5d0ddef3f8a'
city_name = 'Paris'
start_date = datetime.now() - timedelta(days=30)
current_date = start_date
end_date = datetime.now()

url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
weather_response = requests.get(url)
weather_data = weather_response.json()

lat = weather_data['coord']['lat']
lon = weather_data['coord']['lon']
air_pollution = []

air_pollution_records = []


while current_date <= end_date:
    # 12h
    specific_time = current_date.replace(hour=12, minute=0, second=0)
    print(specific_time)
    air_pollution_url = f'https://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={int(specific_time.timestamp())}&end={int(specific_time.timestamp())}&appid={api_key}'

    air_pollution_response = requests.get(air_pollution_url)
    air_pollution_data = air_pollution_response.json()

    for entry in air_pollution_data['list']:
        record = {
            'date': datetime.utcfromtimestamp(entry['dt']).strftime('%Y-%m-%d'),
            'AQI': entry['main']['aqi']
        }#  %H:%M:%S
        record.update(entry['components'])
        air_pollution_records.append(record)

    current_date += timedelta(days=1)

csv_file = 'air_pollution_data.csv'
with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['date', 'AQI', 'co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3'])
    writer.writeheader()
    for record in air_pollution_records:
        writer.writerow(record)

for record in air_pollution_records:
    print(record)
