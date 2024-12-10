import requests
from main import api_keys
API_KEY = api_keys()["key"]


def req(city):
    """Получение кординат"""
    location_url = f'http://dataservice.accuweather.com/locations/v1/cities/search?apikey={API_KEY}&q={city}&language=ru'
    try:
        response = requests.get(location_url)
        data = response.json()
        print(data)
        if data:
            lat = data[0]['GeoPosition']['Latitude']
            long = data[0]['GeoPosition']['Longitude']
            return [lat, long]
    except requests.exceptions.RequestException as e:
        print(f'Ошибка запроса: {e}')
        return None


def get_location_key(city):
    """Функция для получения гео-ключа по кординатам"""
    city = f'{city[0]},{city[1]}'
    location_url = f'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={API_KEY}&q={city}'
    try:
        response = requests.get(location_url)
        data = response.json()
        if data:
            return [data['Key'], data['AdministrativeArea']['LocalizedName']]
    except requests.exceptions.RequestException as e:
        print(f'Ошибка запроса: {e}')
        return None


def get_weather(location_key):
    '''Фукция получения данных о погоде'''
    weather_url = f'http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={API_KEY}&details=true'  # запрос к api
    try:
        weather_request = requests.get(weather_url)  # get-запрос к api
        weather_data = weather_request.json()[0]
        temperature_celsius = weather_data['Temperature']['Metric']['Value']
        humidity_percentage = weather_data['RelativeHumidity']
        wind_speed = round(weather_data['Wind']['Speed']['Metric']['Value'] * 0.2778, 2)
        precipitation_probability = 0 if not weather_data['HasPrecipitation'] else 100
        weather_info = {
            'temperature_celsius': temperature_celsius,
            'humidity_percentage': f'{humidity_percentage}%',
            'wind_speed': wind_speed,
            'precipitation_probability': precipitation_probability
        }
        return weather_info
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса погода: {e}")

