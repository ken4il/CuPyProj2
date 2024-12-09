def check_bad_weather(weather_info:dict):
    '''Функция анализа погодных условий'''
    if weather_info['temperature_celsius'] <= 0:
        return 'Низкая температура, не забудь надеть шапку'
    elif weather_info['temperature_celsius'] >= 30:
        return 'Очень жарко, возьми какой нибудь прохладительный напиток и купи маленький вентилятор с питанием от телефона'
    elif weather_info['wind_speed'] >= 10:
        return 'На улице сильный ветер, отгони машину подальше от деревьев и сиди дома'
    elif weather_info['precipitation_probability'] >= 70:
        return 'Высокая вероятность дождя, у тебя же есть зонтик?'
    else:
        return 'Все чикибамбони, иди погуляй, траву потрогай'