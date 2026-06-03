from datetime import datetime
import logging
from pydantic import BaseModel

from back_end.enums.destination import Destination
from back_end.enums.ticket_status import Ticket_status

from back_end.model.item import Item

class Ticket(BaseModel):
    """
    A "Ticket" is a group of "Items" which can be sent to a destination to prepare. It is linked to a specific order.
    """
    ticket_id: int
    order_id: int
    destination: Destination
    status: Ticket_status = Ticket_status.PENDING
    items: list[Item] = []
    comment: str = ""
    time_at_creation: datetime = datetime.now()
    creator: str = ""

    def __str__(self) -> str:
        items_str = ", ".join(str(item) for item in self.items)
        return (f"Ticket(ticket_id={self.ticket_id}, order_id={self.order_id}, status={self.status}, "
                f"destination={self.destination}, items=[{items_str}], comment='{self.comment}', "
                f"time_at_creation={self.time_at_creation}, creator={self.creator})")
    
    def serialize(self) -> dict:
        return {
            "ticket_id": self.ticket_id,
            "order_id": self.order_id,
            "status": self.status,
            "destination": self.destination,
            "items": [item.serialize() for item in self.items],
            "comment": self.comment,
            "time_at_creation": self.time_at_creation.isoformat(),
            "creator": self.creator
        }
    
    @staticmethod
    def deserialize(data: dict):
        items = [Item.deserialize(item_data) for item_data in data["items"]]
        return Ticket(ticket_id=data["ticket_id"], order_id=data["order_id"], destination=data["destination"], status=data["status"], items=items, comment=data["comment"], time_at_creation=datetime.fromisoformat(data["time_at_creation"]), creator=data["creator"])
    
    """
    The nessecairy getters and setters
    """

    def get_ticket_id(self) -> int:
        return self.ticket_id

    def get_order_id(self) -> int:
        return self.order_id

    def get_status(self) -> Ticket_status:
        return self.status
    
    def set_status(self, status: Ticket_status) -> None:
        self.status = status
        return

    def get_destination(self) -> Destination:
        return self.destination

    def get_items(self) -> list[Item]:
        return self.items
    
    def set_items(self, items: list[Item]) -> None:
        self.items = items
        return

    def get_comment(self) -> str:
        return self.comment
    
    def set_comment(self, comment: str) -> None:
        self.comment = comment
        return

    def get_time_at_creation(self) -> datetime:
        return self.time_at_creation

    def get_creator(self) -> str:
        return self.creator
    
    """
    Other methods
    """

    def add_items(self, items: list[Item]) -> None:
        if any(item is None for item in items):
            logging.error("Items cannot contain None values")
            raise ValueError("Items cannot contain None values")
        self.items.extend(items)
        return
    
    def remove_items(self, items: list[Item]) -> None:
        for item in items:
            try:
                self.items.remove(item)
            except ValueError:
                logging.warning(f"Item {item} not found in ticket {self.ticket_id}")
        return
