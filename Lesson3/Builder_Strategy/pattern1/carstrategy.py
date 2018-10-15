import abc
from random import randint
import competitors

class Weather:
    @property
    def wind_speed(self):
        return randint(0, 20)


class Context:
    """Интерфейс контекста для клиента"""

    def __init__(self, strategy):
        self._strategy = strategy

    def context_interface(self):
        self._strategy.run()


class Strategy(metaclass=abc.ABCMeta):
    """Контекст использует данный интерфейс для вызова алгоритма, определённого
    конкретной стратегией
    """
    @abc.abstractmethod
    def run(self):
        pass


class CompetitionSportscar(Strategy):
    """Реализация конкретной стратегии"""

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        return instance

    def __init__(self, distance, body):
        self.distance = distance
        self.body = body

    def run(self):
        for car in competitors.ret_comp(self.body):
            competitor_time = 0

            for distance in range(self.distance):
                weather = Weather()
                _wind_speed = weather.wind_speed

                if competitor_time == 0:
                    _speed = 1
                else:
                    _speed = (competitor_time / car._Car__time_to_max.seconds) * car._Car__max_speed.kmh
                if _speed > _wind_speed:
                    _speed -= (car._Car__drag_coef.percent * _wind_speed)

                competitor_time += float(1) / _speed

            print("Car <%s> result: %f" % (car._Car__name.brand, competitor_time))


class CompetitionSUV(Strategy):
    """Реализация конкретной стратегии"""

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        return instance

    def __init__(self, distance, body):
        self.distance = distance
        self.body = body

    def run(self):
        for car in competitors.ret_comp(self.body):
            competitor_time = 0

            for distance in range(self.distance):
                weather = Weather()
                _wind_speed = weather.wind_speed

                if competitor_time == 0:
                    _speed = 1
                else:
                    _speed = (competitor_time / car._Car__time_to_max.seconds) * car._Car__max_speed.kmh
                if _speed > _wind_speed:
                    _speed -= (car._Car__drag_coef.percent * _wind_speed)

                competitor_time += float(1) / _speed * car._Car__enginewear.ewf

            print("Car <%s> result: %f" % (car._Car__name.brand, competitor_time))



def start(distance, body):

    """Клиент создаёт реализацию конкретной стратегии с методом объекта algorithm_interface().
    Далее создаётся объект context, аргументом для которого служит конкретная стратегия.
    Через свой метод context_interface(), контекст исполняет метод algorithm_interface()
    конкретной стратегии.
    Тем самым клиент не действует напрямую с конкретной реализацией алгоритма
    """
    if body == 'sportscar':
        print('Competition of sportscar: \n')
        competition_sportscar = CompetitionSportscar(distance, body)
        context = Context(competition_sportscar)
        context.context_interface()

    elif body == 'SUV':
        print('Competition of SUV: \n')
        competition_suv = CompetitionSUV(distance, body)
        context = Context(competition_suv)
        context.context_interface()
