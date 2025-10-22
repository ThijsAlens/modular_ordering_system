# This file contains helper functions for the REST API

import json

from back_end.REST_API.config import FILEWRITERS
from back_end.model.order import Order



def get_order_by_id(order_id: int) -> Order | None:
    orders: list[Order] = FILEWRITERS["JSON_statefiles/orders.json"].read_everything_from_file(Order)
    if orders is None:
        return None
    
    for order in orders:
        if order.order_id == order_id:
            return order

    return None