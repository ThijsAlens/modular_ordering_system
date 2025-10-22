from enum import Enum, auto

class Destination(str, Enum):
    KITCHEN = "kitchen"
    BAR = "bar"
    DESSERT = "dessert"