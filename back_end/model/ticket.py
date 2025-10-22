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
    timestamp: datetime = datetime.now()

    def __str__(self) -> str:
        items_str = ", ".join(str(item) for item in self.items)
        return (f"Ticket(ticket_id={self.ticket_id}, order_id={self.order_id}, status={self.status}, "
                f"destination={self.destination}, items=[{items_str}], comment='{self.comment}', "
                f"timestamp={self.timestamp})")
    
    def serialize(self) -> dict:
        return {
            "ticket_id": self.ticket_id,
            "order_id": self.order_id,
            "status": self.status,
            "destination": self.destination,
            "items": [item.serialize() for item in self.items],
            "comment": self.comment,
            "timestamp": self.timestamp.isoformat()
        }
    
    @staticmethod
    def deserialize(data: dict):
        items = [Item.deserialize(item_data) for item_data in data["items"]]
        return Ticket(ticket_id=data["ticket_id"], order_id=data["order_id"], destination=data["destination"], status=data["status"], items=items, comment=data["comment"], timestamp=datetime.fromisoformat(data["timestamp"]))
    
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

    def get_comment(self) -> str:
        return self.comment
    
    def set_comment(self, comment: str) -> None:
        self.comment = comment
        return

    def get_timestamp(self) -> datetime:
        return self.timestamp
    
    """
    Other methods
    """

    def add_item(self, item: Item) -> None:
        if item is None:
            logging.error("Item cannot be None")
            raise ValueError("Item cannot be None")
        self.items.append(item)
        return
    
    def remove_item(self, item: Item) -> None:
        self.items.remove(item)
        return
