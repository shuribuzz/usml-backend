запуск: docker-compose up

Применены паттерны "Строитель" и "Стратегия". Было принято решение о разделении соревнований на 2 вида - спорткары и внедорожники.
Строитель применяется для построения объекта каждого класса автомобиля со своими характеристиками. Соответственно, расчёт проведения гонки
для каждого класса свой. Здесь и применяется Стратегия.
При запуске соревнования выбирается дистанция и класс гонки: carstrategy.start(10000, 'sportscar') или carstrategy.start(10000, 'SUV').