from enum import Enum, auto

class Order_status(str, Enum):
    ACTIVE = "active"
    PAYED = "payed"
    CANCELED = "canceled"