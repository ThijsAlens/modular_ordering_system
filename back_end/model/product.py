from pydantic import BaseModel

from back_end.enums.destination import Destination
from back_end.enums.product_group import Product_group

class Product(BaseModel):
    """
    A "Product" is a single thing that can be used in an ordered, for example a glass of water or a pancake.
    Something that is on the menu, to actually order products, an "Item" is needed.
    """
    product_id: int
    name: str
    price: float
    destination: Destination
    group: Product_group = Product_group.NO_GROUP
    is_active: bool = True

    """
    Some generic functions to easily print, serialize and deserialize objects
    """
    def __str__(self) -> str:
        return f"Product(product_id={self.product_id}, name={self.name}, price={self.price}, destination={self.destination}, group={self.group}, is_active={self.is_active})"

    def serialize(self) -> dict:
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "destination": self.destination.name,
            "group": self.group.name,
            "is_active": self.is_active
        }
    
    @staticmethod
    def deserialize(data):
        return Product(product_id=data["product_id"], name=data["name"], price=data["price"], destination=data["destination"], group=data["group"], is_active=data["is_active"])
    

    """
    The nessecairy getters and setters
    """
    def get_product_id(self) -> int:
        return self.product_id

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> float:
        return self.price

    def get_group(self) -> Product_group:
        return self.group

    def get_destination(self) -> Destination:
        return self.destination

    def get_is_active(self) -> bool:
        return self.is_active

    def deactivate(self) -> None:
        self.is_active = False

    def activate(self) -> None:
        self.is_active = True