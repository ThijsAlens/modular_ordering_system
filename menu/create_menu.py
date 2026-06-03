# Little script to create products for the menu
import json

from back_end.enums.destination import Destination
from back_end.enums.product_group import Product_group
from back_end.model.menu import Menu
from back_end.model.product import Product

def write_menu_to_file(menu: Menu, file_path: str) -> None:
    with open(file_path, "w") as f:
        json.dump(menu.serialize(), f, indent=4)

def main():
    product_id = 0
    destination = Destination.KITCHEN
    group = Product_group.NO_GROUP
    is_active = True
    file_path = "menu/kitchen.json"

    products: list[Product] = []

    print(f"Currently creating products for the {destination.name} menu, starting with product ID {product_id}. To save, type 'save' when asked for a product name.\n")

    while True:
        name = input("Product name: ")
        if name.lower() == "save":
            break
        price = float(input("Product price: "))
        print(f"Added Product - Product_id: {product_id}, Name: {name}, Price: {price}, Destination: {destination.name}, Group: {group.name}, Active: {is_active}\n")
        products.append(Product(product_id=product_id, name=name, price=price, destination=destination, group=group, is_active=is_active))
        product_id += 1
    
    write_menu_to_file(Menu(destination=destination, products=products), file_path)
if __name__ == "__main__":
    main()