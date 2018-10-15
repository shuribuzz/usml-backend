from random import randint

finish_list = []

class Cars(object):
    CAR_SPECS = {
        'ferrary': {"max_speed": 340, "drag_coef": 0.324, "time_to_max": 26},
        'bugatti': {"max_speed": 407, "drag_coef": 0.39, "time_to_max": 32},
        'toyota': {"max_speed": 180, "drag_coef": 0.25, "time_to_max": 40},
        'lada': {"max_speed": 180, "drag_coef": 0.32, "time_to_max": 56},
        'sx4': {"max_speed": 180, "drag_coef": 0.33, "time_to_max": 44},
    }


class Weather:
    @property
    def wind_speed(self):
        return randint(0, 20)


class Competition:
    """базовый класс, который подлежит обёртыванию"""
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        return instance

    def __init__(self, distance):
        self.distance = distance

    def start(self):
        for competitor_name in competitors:
            competitor_time = 0
            car = Cars().CAR_SPECS[competitor_name]

            for distance in range(self.distance):
                weather = Weather()
                _wind_speed = weather.wind_speed

                if competitor_time == 0:
                    _speed = 1
                else:
                    _speed = (competitor_time / car["time_to_max"]) * car['max_speed']
                    if _speed > _wind_speed:
                        _speed -= (car["drag_coef"] * _wind_speed)

                competitor_time += float(1) / _speed

            print("Car <%s> result: %f" % (competitor_name, competitor_time))
            finish_list.append(competitor_time)
        return finish_list


class Decorator(Competition):
    """Класс декоатора с добавленной функциональностью"""
    def __init__(self, wrapped):
        self._wrapped = wrapped

    print('Finish!' + '\n')
    def start(self):
        print('\n' + 'Лучший результат: {}'.format(min(self._wrapped.start())))



competitors = ('ferrary', 'bugatti', 'toyota', 'lada', 'sx4')
c = Competition(10000)
d_c = Decorator(c)
#c.start()
d_c.start()