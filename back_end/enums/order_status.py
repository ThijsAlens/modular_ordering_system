from enum import Enum, auto

class Order_status(Enum):
    ACTIVE = auto()
    PAYED = auto()
    CANCELED = auto()