import logging

from model.product import Product

class Item:
    """
    An "Item" is a specific product that has been selected for an order, along with any special instructions or comments.
    """
    def __init__(self, product: Product, comment: str = ""):
        if product is None:
            logging.error("Product can't be None.")
            raise ValueError("Product cannot be None")
        self.product: Product = product
        self.comment: str = comment


    """
    Some generic functions to easily print, serialize and deserialize objects
    """
    def __str__(self):
        return f"Item(product={str(self.product)}, comment={self.comment})"
    
    def serialize(self) -> dict:
        return {
            "product": self.product,
            "comment": self.comment
        }
    
    @staticmethod
    def deserialize(data: dict):
        return Item(product=data["product"], comment=data["comment"])


    """
    The nessecairy getters and setters
    """
    def get_product(self) -> Product:
        return self.product
    
    def get_comment(self) -> str:
        return self.comment

    def set_comment(self, comment: str) -> None:
        self.comment = comment
        return
    