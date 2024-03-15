import requests
import csv
from datetime import datetime, timedelta

api_key = 'c96bb98a69fc64d39530c5d0ddef3f8a'
city_name = 'Paris'

start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()

url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'

weather_data = []

current_date = start_date
while current_date <= end_date:
    response = requests.get(url)
    data = response.json()

    temperature = data['main']['temp']
    wind_speed = data['wind']['speed']
    humidity = data['main']['humidity']
    timestamp = data['dt']

    formatted_date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    weather_data.append({
        'date': formatted_date,
        'temperature': temperature,
        'wind_speed': wind_speed,
        'humidity': humidity
    })

    current_date = current_date + timedelta(hours=1)

for data in weather_data:
    print(f"date: {data['date']}, Temperature: {data['temperature']}°C, Wind Speed: {data['wind_speed']} m/s, Humidity: {data['humidity']}%")

csv_file = 'weather_data2.csv'
with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['date', 'temperature', 'wind_speed', 'humidity'])
    writer.writeheader()
    for data in weather_data:
        writer.writerow(data)
