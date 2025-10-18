from datetime import datetime

from back_end.model.ticket import Ticket
from back_end.enums.order_status import Order_status

class Order:
    """
    An "Order" is a collection of "Tickets" associated with a specific table or customer.
    """
    def __init__(self, order_id: int, table_number: int = -1, timestamp: datetime = None, tickets: list[Ticket] = [], status: Order_status = Order_status.ACTIVE):
        self.id: int = order_id
        self.table_reference: str = table_number
        self.timestamp: datetime = timestamp
        self.tickets: list[Ticket] = tickets
        self.status: Order_status = status

    def __str__(self) -> str:
        tickets_str = ", ".join(str(ticket) for ticket in self.tickets)
        return (f"Order(id={self.id}, table_number={self.table_reference}, timestamp={self.timestamp}, "
                f"tickets=[{tickets_str}], status={self.status})")
    
    def serialize(self) -> dict:
        return {
            "id": self.id,
            "table_reference": self.table_reference,
            "timestamp": self.timestamp,
            "tickets": [ticket.serialize() for ticket in self.tickets],
            "status": self.status.name
        }
    
    @staticmethod
    def deserialize(data: dict):
        tickets = [Ticket.deserialize(ticket_data) for ticket_data in data["tickets"]]
        return Order(order_id=data["id"], table_number=data["table_reference"], timestamp=data["timestamp"], tickets=tickets, status=Order_status[data["status"]])
    
    """
    The nessecairy getters and setters
    """

    def get_id(self) -> int:
        return self.id

    def get_table_reference(self) -> str:
        return self.table_reference

    def get_timestamp(self) -> datetime:
        return self.timestamp

    def get_tickets(self) -> list[Ticket]:
        return self.tickets

    def get_status(self) -> Order_status:
        return self.status

    def set_status(self, status: Order_status) -> None:
        if status is None:
            raise ValueError("Status cannot be None")
        self.status = status

    """
    Other methods
    """

    def add_ticket(self, ticket: Ticket) -> None:
        if ticket is None:
            raise ValueError("Ticket cannot be None")
        self.tickets.append(ticket)

    def remove_ticket(self, ticket: Ticket) -> None:
        self.tickets.remove(ticket)