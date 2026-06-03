

from pydantic import BaseModel

from back_end.enums.destination import Destination
from back_end.model.product import Product


class Menu(BaseModel):
    """
    The "Menu" class represents the menu of a restaurant, which consists of a list of "Products" that are available for customers to order.
    """
    
    destination: Destination
    products: list[Product]

    def __str__(self) -> str:
        products_str = ", ".join(str(product) for product in self.products)
        return f"Menu(destination={self.destination}, products=[{products_str}])"
    
    def serialize(self) -> dict:
        return {
            "destination": self.destination,
            "products": [product.serialize() for product in self.products]
        }
    
    @staticmethod
    def deserialize(data: dict):
        products = [Product.deserialize(product_data) for product_data in data["products"]]
        return Menu(destination=data["destination"], products=products)
    
    """
    The nessecairy getters and setters
    """

    def get_destination(self) -> Destination:
        return self.destination
    
    def get_products(self) -> list[Product]:
        return self.products