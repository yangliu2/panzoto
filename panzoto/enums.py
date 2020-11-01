""" Set up enums to eliminate magic strings """

from enum import Enum, auto


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        """
        the value of the ENUM now become the lower case of the name
        :params: left because parent class has them
        """
        return name.lower()

class Names(AutoName):
    PANZOTO = auto()

class Gender(AutoName):
    FEMALE = auto()
    MALE = auto()

class Logging(AutoName):
    INFO = auto()
    WARNING = auto()
    DEBUG = auto()
    ERROR = auto()

class People(AutoName):
    FIRST_NAME = "First name"
    LAST_NAME = "Last name"
    ID = "ID"
    GENDER = "Gender"
    HEALTH = "Health"
    ENERGY = "Energy"
    POSESSIONS = "Posessions"

class FoodStatus(AutoName):
    FOOD_VALUE = "Food value"
    NAME = "Name"
    OWNER = "Owner"
    ID = "ID"