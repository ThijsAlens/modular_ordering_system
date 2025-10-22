from datetime import datetime
from pydantic import BaseModel

from back_end.model.ticket import Ticket
from back_end.enums.order_status import Order_status

class Order(BaseModel):
    """
    An "Order" is a collection of "Tickets" associated with a specific table or customer.
    """
    
    order_id: int
    table_reference: str
    time_at_creation: datetime = datetime.now()
    tickets: list[Ticket] = []
    status: Order_status = Order_status.ACTIVE

    def __str__(self) -> str:
        tickets_str = ", ".join(str(ticket) for ticket in self.tickets)
        return (f"Order(order_id={self.order_id}, table_reference={self.table_reference}, time_at_creation={self.time_at_creation}, "
                f"tickets=[{tickets_str}], status={self.status})")
    
    def serialize(self) -> dict:
        return {
            "order_id": self.order_id,
            "table_reference": self.table_reference,
            "time_at_creation": self.time_at_creation.isoformat(),
            "tickets": [ticket.serialize() for ticket in self.tickets],
            "status": self.status.name
        }
    
    @staticmethod
    def deserialize(data: dict):
        tickets = [Ticket.deserialize(ticket_data) for ticket_data in data["tickets"]]
        return Order(order_id=data["order_id"], table_reference=data["table_reference"], time_at_creation=datetime.fromisoformat(data["time_at_creation"]), tickets=tickets, status=Order_status[data["status"]])
    
    """
    The nessecairy getters and setters
    """

    def get_order_id(self) -> int:
        return self.order_id

    def get_table_reference(self) -> str:
        return self.table_reference

    def get_time_at_creation(self) -> datetime:
        return self.time_at_creation

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