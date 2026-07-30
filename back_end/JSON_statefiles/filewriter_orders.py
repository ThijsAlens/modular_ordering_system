

from back_end.JSON_filewriter.JSON_filewriter import JSON_Filewriter
from back_end.enums.destination import Destination
from back_end.model.order import Order
from back_end.model.ticket import Ticket


class Filewriter_orders(JSON_Filewriter):
    """
    A class for managing the "orders.json" state file.
    """

    def __init__(self, file_path: str):
        super().__init__(file_path)

    def get_order_by_id(self, order_id: int) -> Order | None:
        orders: list[Order] = self.read_everything_from_file(Order)
        if orders is None:
            return None

        for order in orders:
            if order.order_id == order_id:
                return order

        return None

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
    
    def get_ticket_by_ids(self, order_id: int, ticket_id: int) -> Ticket | None:
        orders: list[Order] = self.read_everything_from_file(Order)
        for order in orders:
            if order.get_order_id() == order_id:
                for ticket in order.get_tickets():
                    if ticket.get_ticket_id() == ticket_id:
                        return ticket
        return None
    
    def update_ticket_by_ids(self, order_id: int, ticket_id: int, ticket: Ticket) -> Order | None:
        orders: list[Order] = self.read_everything_from_file(Order)
        for order in orders:
            if order.get_order_id() == order_id:
                for idx, existing_ticket in enumerate(order.get_tickets()):
                    if existing_ticket.get_ticket_id() == ticket_id:
                        order.get_tickets()[idx] = ticket
                        return order
        return None
    
    def get_all_pending_tickets(self) -> list[Ticket]:
        orders: list[Order] = self.read_everything_from_file(Order)
        pending_tickets: list[Ticket] = []
        for order in orders:
            for ticket in order.get_tickets():
                if ticket.get_status() == "pending":
                    pending_tickets.append(ticket)
        return pending_tickets
    
    def get_all_pending_tickets_by_destination(self, destination: Destination) -> list[Ticket]:
        orders: list[Order] = self.read_everything_from_file(Order)
        pending_tickets: list[Ticket] = []
        for order in orders:
            for ticket in order.get_tickets():
                if ticket.get_status() == "pending" and ticket.get_destination() == destination:
                    pending_tickets.append(ticket)
        return pending_tickets

    def get_all_completed_tickets_by_destination(self, destination: Destination) -> list[Ticket]:
        orders: list[Order] = self.read_everything_from_file(Order)
        completed_tickets: list[Ticket] = []
        for order in orders:
            for ticket in order.get_tickets():
                if ticket.get_status() == "completed" and ticket.get_destination() == destination:
                    completed_tickets.append(ticket)
        return completed_tickets