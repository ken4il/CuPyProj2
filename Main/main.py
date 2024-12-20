import json
from flask import Flask, render_template, request, flash
from get_cord_and_weather import *
from check_weather import check_bad_weather


def api_keys():
    with open('key.json', 'r') as file:
        data = json.load(file)
    return data


try:
    api_key = api_keys()["key"]
except Exception:
    print('Не найден файл key.json с указанием api ключа')
    exit(0)

app = Flask(__name__)


# Пример координат

def making_json(city):
    city = req(city=city)
    cor = get_location_key(city=city)[0]
    weather = get_weather(cor)
    return weather


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        try:
            city_a = request.form['Город_a']
            city_b = request.form['Город_b']
        except Exception:
            return render_template('error.html', msg='ошибка формы')
        try:
            if not city_a or not city_b:
                return render_template('error.html', msg='Города не указаны, повторите ввод')

        except ValueError as VE:
            return render_template('error.html', msg='Города не указаны неправильно')

        try:
            response_a = making_json(city_a)
            response_b = making_json(city_b)
        except Exception:
            return render_template('error.html', msg='Ошибка запросов к API')

        if isinstance(response_a, str) and response_a.startswith("Request error"):
            return render_template('error.html', msg='Ошибка запроса на API')
        elif isinstance(response_a, str):
            return render_template('error.html', msg='Нет данных с сервера')

        # Предполагаем, что making_json возвращает данные в нужном формате
        # Проверяем погоду для города a
        try:
            favorability_a = check_bad_weather(response_a)
            temperature_celsius_a = response_a["temperature_celsius"]
            wind_speed_a = response_a['wind_speed']
            humidity_percentage_a = response_a['humidity_percentage']
            precipitation_probability_a = response_a['precipitation_probability']

            # Создаем словарь weather_info для города a
            weather_info_a = {
                'temperature_celsius': temperature_celsius_a,
                'humidity_percentage': f'{humidity_percentage_a}',
                'wind_speed': wind_speed_a,
                'precipitation_probability': precipitation_probability_a
            }

            # Проверяем погоду для города b
            favorability_b = check_bad_weather(response_b)
            temperature_celsius_b = response_b["temperature_celsius"]
            wind_speed_b = response_b['wind_speed']
            humidity_percentage_b = response_b['humidity_percentage']
            precipitation_probability_b = response_b['precipitation_probability']

            # Создаем словарь wet_info для города b
            weather_info_b = {
                'temperature_celsius': temperature_celsius_b,
                'humidity_percentage': f'{humidity_percentage_b}',
                'wind_speed': wind_speed_b,
                'precipitation_probability': precipitation_probability_b
            }
        except Exception:
            return render_template('error.html', msg='Ошибка получения данных с API')

        return render_template('form.html', weather_info_a=weather_info_a, weather_info_b=weather_info_b,
                               favorability_a=favorability_a, favorability_b=favorability_b)

    return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True)
