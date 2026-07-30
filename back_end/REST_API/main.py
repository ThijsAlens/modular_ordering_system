from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


from datetime import datetime
from pathlib import Path
import json
import logging
import os

from back_end.config import FILEMANAGER_SEQUENCE, LOGGER, FILEMANAGER_ORDERS, FILEMANAGER_MENU, FILEMANAGER_FINISHED_ORDERS, MODE

from back_end.enums.order_status import Order_status
from back_end.enums.destination import Destination
from back_end.enums.ticket_status import Ticket_status
from back_end.model.item import Item
from back_end.model.menu import Menu
from back_end.model.order import Order
from back_end.model.ticket import Ticket

# Set logging level based on environment
if os.getenv("APP_ENV", "production") == "development":
    LOGGER.info("Running in development mode. Setting variables for development.")
    LOGGER.setLevel(logging.DEBUG)
    MODE = "development"
else:
    # clear log-file
    with open("back_end/back_end.log", 'w'):
        pass
    LOGGER.info("Running in production mode. Setting variables for production.")
    LOGGER.setLevel(logging.INFO)
    MODE = "production"

# Initialize FastAPI app
back_end = FastAPI(debug=(os.getenv("APP_ENV", "production")=="development"))
back_end.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@back_end.get("/")
def root():
    return {"message": "Welcome to the back_end REST API. Visit \"/docs\" for the API documentation."}

# --------------------------------- #
#         Order handeling           #
# --------------------------------- #
@back_end.get("/get_order_by_id")
def get_order_by_id(order_id: int):
    LOGGER.info(f"Handeling \"get_order_by_id\" request for order ID: {order_id}")
    order: Order | None = FILEMANAGER_ORDERS.get_order_by_id(order_id)
    if order is None:
        LOGGER.error(f"Order with ID {order_id} not found.")
        raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found.")
    return order.serialize()

@back_end.get("/get_orders_by_table_reference")
def get_orders_by_table_reference(table_reference: str):
    LOGGER.info(f"Handeling \"get_orders_by_table_reference\" request for table reference: {table_reference}")
    orders: list[Order] = FILEMANAGER_ORDERS.read_everything_from_file(Order)
    matching_orders = [order.serialize() for order in orders if order.get_table_reference() == table_reference]
    if not matching_orders:
        LOGGER.error(f"Orders for table reference {table_reference} not found.")
        raise HTTPException(status_code=404, detail=f"No active orders found for table reference {table_reference}.")
    return matching_orders

@back_end.post("/create_new_order")
def create_new_order(table_reference: str):
    LOGGER.info(f"Handeling \"create_new_order\" request for table reference: {table_reference}")
    new_order_id = FILEMANAGER_SEQUENCE.get_next_order_id()
    new_order = Order(order_id=new_order_id, table_reference=table_reference, time_at_creation=datetime.now(), tickets=[], status=Order_status.ACTIVE)
    FILEMANAGER_ORDERS.add_order(new_order)
    return new_order.serialize()

@back_end.post("/change_order_status_by_id")
def change_order_status_by_id(order_id: int, new_status: Order_status):
    """If an order is changed to PAYED, it is backed up to finished_orders.json and removed from orders.json."""
    LOGGER.info(f"Handeling \"change_order_status\" request for order ID: {order_id} to new status: {new_status}")
    order: Order = Order.deserialize(get_order_by_id(order_id))
    order.set_status(new_status)
    if order.get_status() == Order_status.PAYED:
        FILEMANAGER_FINISHED_ORDERS.add_order(order)
        FILEMANAGER_ORDERS.remove_order_by_id(order_id)
    else:
        FILEMANAGER_ORDERS.remove_order_by_id(order_id)
        FILEMANAGER_ORDERS.add_order(order)
    return {"message": f"Order with ID {order_id} status changed to {new_status}."}

# --------------------------------- #
#         Ticket handeling          #
# --------------------------------- #
@back_end.post("/create_new_ticket")
def create_new_ticket(order_id: int, destination: Destination, items: list[Item], comment: str = "", last_editor: str = ""):
    LOGGER.info(f"Handeling \"create_new_empty_ticket\" request")
    order: Order = Order.deserialize(get_order_by_id(order_id))
    
    new_ticket_id = FILEMANAGER_SEQUENCE.get_next_ticket_id()
    new_ticket = Ticket(ticket_id=new_ticket_id, order_id=order_id, destination=destination, items=items, comment=comment, last_editor=last_editor)
    
    order.get_tickets().append(new_ticket)
    FILEMANAGER_ORDERS.remove_order_by_id(order.get_order_id())
    FILEMANAGER_ORDERS.add_order(order)

    return new_ticket.serialize()

@back_end.get("/get_ticket_by_ids")
def get_ticket_by_ids(order_id: int, ticket_id: int):
    LOGGER.info(f"Handeling \"get_ticket_by_ids\" request for order ID: {order_id} and ticket ID: {ticket_id}")
    order: Order | None = FILEMANAGER_ORDERS.get_order_by_id(order_id)
    if order is None:
        LOGGER.error(f"Order with ID {order_id} not found.")
        raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found.")
    
    for ticket in order.get_tickets():
        if ticket.get_ticket_id() == ticket_id:
            return ticket.serialize()
    
    LOGGER.error(f"Ticket with ID {ticket_id} not found in order with ID {order_id}.")
    raise HTTPException(status_code=404, detail=f"Ticket with ID {ticket_id} not found in order with ID {order_id}.")

@back_end.post("/update_ticket")
def update_ticket(new_ticket: Ticket):
    LOGGER.info(f"Handeling \"update_items_in_ticket_by_id\" request for ticket ID: {new_ticket.get_ticket_id()}")
    # Update the order that contains this ticket
    order: Order | None = FILEMANAGER_ORDERS.update_ticket_by_ids(new_ticket.get_order_id(), new_ticket.get_ticket_id(), new_ticket)
    if order is None:
        LOGGER.error(f"Could not update ticket with ID {new_ticket.get_ticket_id()} in order with ID {new_ticket.get_order_id()}.")
        raise HTTPException(status_code=404, detail=f"Could not update ticket with ID {new_ticket.get_ticket_id()} in order with ID {new_ticket.get_order_id()}.")
    
    FILEMANAGER_ORDERS.remove_order_by_id(order.get_order_id())
    FILEMANAGER_ORDERS.add_order(order)

    return new_ticket.serialize()

@back_end.get("/get_all_pending_tickets_by_destination")
def get_all_pending_tickets_by_destination(destination: Destination):
    LOGGER.info(f"Handling \"get_all_pending_tickets_by_destination\" request for destination: {destination}")
    pending_tickets = FILEMANAGER_ORDERS.get_all_pending_tickets_by_destination(destination)
    return [ticket.serialize() for ticket in pending_tickets]

@back_end.get("/get_all_completed_tickets_by_destination")
def get_all_completed_tickets_by_destination(destination: Destination):
    LOGGER.info(f"Handling \"get_all_completed_tickets_by_destination\" request for destination: {destination}")
    completed_tickets = FILEMANAGER_ORDERS.get_all_completed_tickets_by_destination(destination)
    return [ticket.serialize() for ticket in completed_tickets]


@back_end.post("/change_ticket_status_by_ids")
def change_ticket_status_by_ids(order_id: int, ticket_id: int, status: Ticket_status):
    LOGGER.info(f"Handling \"change_ticket_status_by_ids\" request for order ID: {order_id}, ticket ID: {ticket_id}, and new status: {status}")
    ticket: Ticket | None = FILEMANAGER_ORDERS.get_ticket_by_ids(order_id, ticket_id)
    if ticket is None:
        LOGGER.error(f"Combination of order ID {order_id} and ticket ID {ticket_id} not found.")
        raise HTTPException(status_code=404, detail=f"Combination of order ID {order_id} and ticket ID {ticket_id} not found.")

    ticket.set_status(status)

    # Update the order that contains this ticket
    order: Order | None = FILEMANAGER_ORDERS.update_ticket_by_ids(order_id, ticket_id, ticket)
    if order is None:
        LOGGER.error(f"Could not update ticket with ID {ticket_id} in order with ID {order_id}.")
        raise HTTPException(status_code=404, detail=f"Could not update ticket with ID {ticket_id} in order with ID {order_id}.")

    FILEMANAGER_ORDERS.remove_order_by_id(order.get_order_id())
    FILEMANAGER_ORDERS.add_order(order)

    return ticket.serialize()

# --------------------------------- #
#        Product handeling          #
# --------------------------------- #
@back_end.get("/get_product_by_id")
def get_product_by_id(product_id: int):
    LOGGER.info(f"Handling \"get_product_by_id\" request for product ID: {product_id}")
    menus: list[Menu] = FILEMANAGER_MENU.read_everything_from_file(Menu)
    for menu in menus:
        for product in menu.get_products():
            if product["product_id"] == product_id:
                return product.serialize()
    LOGGER.error(f"Product with ID {product_id} not found in any menu.")
    raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found in any menu.")

# --------------------------------- #
#          Menu handeling           #
# --------------------------------- #
@back_end.get("/get_menu_by_destination")
def get_menu_by_destination(destination: Destination):
    LOGGER.info(f"Handling \"get_menu_by_destination\" request for destination: {destination}")
    menu: Menu | None = FILEMANAGER_MENU.get_menu_by_destination(destination)
    if menu is None:
        LOGGER.error(f"Menu for destination {destination} not found.")
        raise HTTPException(status_code=404, detail=f"Menu for destination {destination} not found.")
    return menu.serialize()

# --------------------------------- #
#    Startup/shutdown handeling     #
# --------------------------------- #
@back_end.on_event("startup")
def startup_event():

    def is_valid_json(file_path: Path) -> bool:
        """Checks if a file contains valid JSON."""
        try:
            with open(file_path, 'r') as f:
                json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return False
        return True

    LOGGER.info("Starting up the back_end REST API...")
    LOGGER.info("Making sure all components are initialized properly.")

    back_end_path = Path.cwd() / "back_end"

    # Check for necessary JSON state files and make sure they are valid JSONs
    if not (back_end_path / "JSON_statefiles" / "active_orders.json").is_file() or is_valid_json(back_end_path / "JSON_statefiles" / "orders.json") is False:
        LOGGER.info("orders.json file not found or corrupted. Creating a new one...")
        with open(back_end_path / "JSON_statefiles" / "orders.json", 'w') as f:
            json.dump([], f)

    if not (back_end_path / "JSON_backup" / "finished_orders.json").is_file() or is_valid_json(back_end_path / "JSON_backup" / "finished_orders.json") is False:
        LOGGER.info("finished_orders.json file not found or corrupted. Creating a new one...")
        with open(back_end_path / "JSON_backup" / "finished_orders.json", 'w') as f:
            json.dump([], f)

    if not (back_end_path / "JSON_statefiles" / "menu.json").is_file() or is_valid_json(back_end_path / "JSON_statefiles" / "menu.json") is False:
        LOGGER.info("menu.json file not found or corrupted. Creating a new one...")
        with open(back_end_path / "JSON_statefiles" / "menu.json", 'w') as f:
            json.dump([], f)

    # Clear the state files and load menu from user given directory
    FILEMANAGER_MENU.clear_file() # always clear the menu to always have the most recent menu from the user
    FILEMANAGER_ORDERS.clear_file() if MODE == "development" else None
    FILEMANAGER_FINISHED_ORDERS.clear_file() if MODE == "development" else None
    FILEMANAGER_SEQUENCE.clear_file() if MODE == "development" else None

    FILEMANAGER_MENU.load_menu_from_user_directory(Path.cwd() / "menu")

    LOGGER.info("All components initialized successfully. Back-end REST API is ready to handle requests.")
    return

@back_end.on_event("shutdown")
def shutdown_event():
    LOGGER.info("Shutting down the back_end REST API...")
    LOGGER.info("NEED TO IMPLEMENT BACKUP ON SHUTDOWN...")
    return