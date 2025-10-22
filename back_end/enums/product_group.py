from enum import Enum, auto

class Product_group(str, Enum):
    NO_GROUP = "no_group"
    FOOD = "food"
    DRINK = "drink"
    DESSERT = "dessert"