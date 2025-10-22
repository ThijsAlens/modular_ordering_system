

from back_end.JSON_filewriter.JSON_filewriter import JSON_Filewriter
from back_end.model.order import Order


class Filewriter_orders(JSON_Filewriter):
    """
    A class for managing the "orders.json" state file.
    """

    def __init__(self, file_path: str):
        super().__init__(file_path)

    def remove_order_by_id(self, order_id: int) -> bool:
        """
        Removes an order from the "orders.json" file by its ID.

        Args:
            order_id (int): The ID of the order to be removed.

        Returns:
            bool: True if the order was found and removed, False otherwise.
        """
        orders: list[Order] = self.read_everything_from_file(Order)
        if orders is None:
            return False

        updated_orders = [order for order in orders if order.get_order_id() != order_id]

        if len(updated_orders) == len(orders):
            return False

        # sort the orders by their ID to maintain order
        updated_orders.sort(key=lambda order: order.get_order_id())

        self.append_to_file(updated_orders, truncate=True)
        return True
    
    def add_order(self, order: Order) -> None:
        """
        Adds a new order to the "orders.json" file.

        Args:
            order (Order): The order to be added.

        Returns:
            None
        """
        curr_orders: list[Order] = self.read_everything_from_file(Order)
        curr_orders.append(order)

        # sort the orders by their ID to maintain order
        curr_orders.sort(key=lambda order: order.get_order_id())
        self.append_to_file(curr_orders, truncate=True)
        return