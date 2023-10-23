import geocoder
import requests
def get_weather():
    g = geocoder.ip('me')
    print(f"City: {g.city}, State: {g.state}, Latitude: {g.lat}, Longitude: {g.lng}")
    city = g.city
    city = 'Mangalore'#REMEBER TO REMOVE THIS
    print(city)
    URL = f"http://api.weatherapi.com/v1/current.json?key=67859d3bc72046bcb9783007231710&q={city}&aqi=no&days=7"
    a = requests.get(URL)
    data = a.json()
    print(data)
    data = data['current']
    print(data['temp_c'])
    print(data['condition']['text'])
    #print(data['condition']['icon'])    
    print(data['wind_kph'])
    print(data['humidity'])
    print(data['pressure_mb'])
    print(data['precip_mm'])
    print(data['cloud'])
    #print(data['feelslike_c'])
    weather = dict()
    weather['current temperature'] = data['temp_c']
    weather['current condition'] = data['condition']['text']
    weather['current wind in kmph'] = data['wind_kph']
    weather['current humidity'] = data['humidity']
    weather['current pressure in mb'] = data['pressure_mb']
    weather['current precipitation in mm'] = data['precip_mm']
    weather['icon'] = data['condition']['icon']


    return weather