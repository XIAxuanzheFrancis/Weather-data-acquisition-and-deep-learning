# https://zhuanlan.zhihu.com/p/646084303
# https://www.geeksforgeeks.org/python-api-tutorial-getting-started-with-apis/#making-api-requests-in-python
import requests
from datetime import datetime, timedelta
import csv

api_key = 'c96bb98a69fc64d39530c5d0ddef3f8a'
city_name = 'Paris'
#  DATE UN MOIS
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()
# https://openweathermap.org/current
# api--->https://pro.openweathermap.org/data/2.5/forecast/climate?q=London&appid={API key}
# Temperature. Unit Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit
url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
#res
weather_data = []


current_date = start_date
while current_date <= end_date:
    response = requests.get(url)
    data = response.json()

    temperature = data['main']['temp']
    wind_speed = data['wind']['speed']
    humidity = data['main']['humidity']

# https://www.geeksforgeeks.org/python-strftime-function/
    weather_data.append({
        'date': current_date.strftime('%Y-%m-%d'),
        'temperature': temperature,
        'wind_speed': wind_speed,
        'humidity': humidity
    })

    current_date = current_date + timedelta(days=1)

for data in weather_data:
    print(f"Date: {data['date']}, Temperature: {data['temperature']}°C, Wind Speed: {data['wind_speed']} m/s, Humidity: {data['humidity']}%")

print("start")
csv_file = 'weather_data.csv'
with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['date', 'temperature', 'wind_speed', 'humidity'])
    writer.writeheader()
    for data in weather_data:
        writer.writerow(data)
print("end")