'''Элементы Car'''
class Name:
    brand = None

class Body:
    shape = None

class MaxSpeed:
    kmh = None

class DragCoef:
    percent = None

class TimeToMax:
    seconds = None

class EngineWear:
    ewf = None



class Car:
    """The final product"""
    def __init__(self):
        self.__name = None
        self.__body = None
        self.__max_speed = None
        self.__drag_coef = None
        self.__time_to_max = None
        self.__enginewear = None


    def setName(self, name):
        self.__name = name

    def setBody(self, body):
        self.__body = body

    def setMaxSpeed(self, max_speed):
        self.__max_speed = max_speed

    def setDragCoef(self, drag_coef):
        self.__drag_coef = drag_coef

    def setTimeToMax(self, time_to_max):
        self.__time_to_max = time_to_max

    def setEngineWear(self, enginewear):
        self.__enginewear = enginewear



class Builder:
    """Интерфейс построения всех элементов Car"""
    def getName(self): pass

    def getBody(self): pass

    def getMaxSpeed(self): pass

    def getDragCoef(self): pass

    def getTimeToMax(self): pass

    def getEngineWear(self): pass



class Director:
    """Построение объекта car. Используется соответствующий билдер"""
    __builder = None

    def setBuilder(self, builder):
        self.__builder = builder

    # The algorithm for assembling a car
    def getCar(self):
        car = Car()

        # First goes the name
        name = self.__builder.getName()
        car.setName(name)

        # Then car body
        body = self.__builder.getBody()
        car.setBody(body)

        # Then max speed
        max_speed = self.__builder.getMaxSpeed()
        car.setMaxSpeed(max_speed)

        # Then drag coef
        drag_coef = self.__builder.getDragCoef()
        car.setDragCoef(drag_coef)

        # Then time to max
        time_to_max = self.__builder.getTimeToMax()
        car.setTimeToMax(time_to_max)

        # Then engine wear factor
        enginewear = self.__builder.getEngineWear()
        car.setEngineWear(enginewear)

        return car



class SportscarBuilder(Builder):
    """Реализация конкретных билдеров для спорткара и внедорожника"""
    def __init__(self, brand, shape, maxspeed, dragcoef, timetomax):
        self.brand = brand
        self.shape = shape
        self.maxspeed = maxspeed
        self.dragcoef = dragcoef
        self.timetomax = timetomax

    def getName(self):
        name = Name()
        name.brand = self.brand
        return name

    def getBody(self):
        body = Body()
        body.shape = self.shape
        return body

    def getMaxSpeed(self):
        max_speed = MaxSpeed()
        max_speed.kmh = self.maxspeed
        return max_speed

    def getDragCoef(self):
        drag_coef = DragCoef()
        drag_coef.percent = self.dragcoef
        return drag_coef

    def getTimeToMax(self):
        time_to_max = TimeToMax()
        time_to_max.seconds = self.timetomax
        return time_to_max


class SUVBuilder(Builder):

    def __init__(self, brand, shape, maxspeed, dragcoef, timetomax, ewf):
        self.brand = brand
        self.shape = shape
        self.maxspeed = maxspeed
        self.dragcoef = dragcoef
        self.timetomax = timetomax
        self.ewf = ewf

    def getName(self):
        name = Name()
        name.brand = self.brand
        return name

    def getBody(self):
        body = Body()
        body.shape = self.shape
        return body

    def getMaxSpeed(self):
        max_speed = MaxSpeed()
        max_speed.kmh = self.maxspeed
        return max_speed

    def getDragCoef(self):
        drag_coef = DragCoef()
        drag_coef.percent = self.dragcoef
        return drag_coef

    def getTimeToMax(self):
        time_to_max = TimeToMax()
        time_to_max.seconds = self.timetomax
        return time_to_max

    def getEngineWear(self):
        enginewear = EngineWear()
        enginewear.ewf = self.ewf
        return enginewear



def create(brand, shape, maxspeed, dragcoef, timetomax, ewf):
    """В зависимости от выбора кузова, директор выбирает соответствующий билдер"""
    director = Director()

    if shape == 'sportscar':
        # Build sportscar
        director.setBuilder(SportscarBuilder(brand, shape, maxspeed, dragcoef, timetomax))
        sportscar = director.getCar()
        return sportscar
    elif shape == 'SUV':
        # Build SUV
        director.setBuilder(SUVBuilder(brand, shape, maxspeed, dragcoef, timetomax, ewf))
        suv = director.getCar()
        return suv
