from datetime import datetime
import logging

from back_end.enums.destination import Destination
from back_end.enums.ticket_status import Ticket_status

from back_end.model.item import Item

class Ticket:
    """
    A "Ticket" is a group of "Items" which can be sent to a destination to prepare. It is linked to a specific order.
    """
    def __init__(self, ticket_id: int, order_id: int, destination: Destination, state: Ticket_status = Ticket_status.PENDING, items: list[Item] = [], comment: str = "", timestamp: datetime = None):
        self.id: int = ticket_id
        self.order_id: int = order_id
        self.state: Ticket_status = state
        self.destination: Destination = destination
        self.items: list[Item] = items
        self.comment: str = comment
        self.timestamp: datetime = timestamp if timestamp is not None else datetime.now()

    def __str__(self) -> str:
        items_str = ", ".join(str(item) for item in self.items)
        return (f"Ticket(id={self.id}, order_id={self.order_id}, state={self.state}, "
                f"destination={self.destination}, items=[{items_str}], comment='{self.comment}', "
                f"timestamp={self.timestamp})")
    
    def serialize(self) -> dict:
        return {
            "id": self.id,
            "order_id": self.order_id,
            "state": self.state,
            "destination": self.destination,
            "items": [item.serialize() for item in self.items],
            "comment": self.comment,
            "timestamp": self.timestamp
        }
    
    @staticmethod
    def deserialize(data: dict):
        items = [Item.deserialize(item_data) for item_data in data["items"]]
        return Ticket(ticket_id=data["id"], order_id=data["order_id"], destination=data["destination"], state=data["state"], items=items, comment=data["comment"], timestamp=data["timestamp"])
    
    """
    The nessecairy getters and setters
    """

    def get_id(self) -> int:
        return self.id

    def get_order_id(self) -> int:
        return self.order_id

    def get_state(self) -> Ticket_status:
        return self.state
    
    def set_state(self, state: Ticket_status) -> None:
        self.state = state
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
