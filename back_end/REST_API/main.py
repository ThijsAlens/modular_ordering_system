from datetime import datetime
from back_end.enums.destination import Destination
from fastapi import FastAPI
from pathlib import Path
import json
import logging

from back_end.REST_API.config import LOGGER, FILEWRITERS
import back_end.REST_API.helper_functions as helper_functions

from back_end.enums.order_status import Order_status
from back_end.model.order import Order
from back_end.model.ticket import Ticket

back_end = FastAPI()

@back_end.get("/")
def root():
    return {"message": "Welcome to the back_end REST API. Visit \"/docs\" for the API documentation."}

@back_end.get("/get_order_by_id")
def get_order_by_id(order_id: int):
    LOGGER.info(f"Handeling \"get_order_by_id\" request for order ID: {order_id}")
    order = helper_functions.get_order_by_id(order_id)
    if order is None:
        LOGGER.error(f"Order with ID {order_id} not found.")
        return {"error": f"Order with ID {order_id} not found."}
    return order.serialize()

@back_end.post("/create_new_order")
def create_new_order(table_reference: str):
    LOGGER.info(f"Handeling \"create_new_order\" request for table number: {table_reference}")
    orders: list[Order] = FILEWRITERS["JSON_statefiles/orders.json"].read_everything_from_file(Order)
    new_order_id = orders[-1].get_order_id() + 1 if len(orders) > 0 else 0
    new_order = Order(order_id=new_order_id, table_reference=table_reference, time_at_creation=datetime.now(), tickets=[], status=Order_status.ACTIVE)
    FILEWRITERS["JSON_statefiles/orders.json"].add_order(new_order)
    return {"message": f"New order created with ID {new_order_id} for table with table number {table_reference}."}

@back_end.post("/change_order_status")
def change_order_status(order_id: int, new_status: Order_status):
    LOGGER.info(f"Handeling \"change_order_status\" request for order ID: {order_id} to new status: {new_status}")
    order = helper_functions.get_order_by_id(order_id)
    if order is None:
        LOGGER.error(f"Order with ID {order_id} not found.")
        return {"error": f"Order with ID {order_id} not found."}
    order.set_status(new_status)
    FILEWRITERS["JSON_statefiles/orders.json"].remove_order_by_id(order_id)
    FILEWRITERS["JSON_statefiles/orders.json"].add_order(order)
    return {"message": f"Order with ID {order_id} status changed to {new_status}."}

@back_end.post("/add_ticket_to_order")
def add_ticket_to_order(order_id: int, ticket: Ticket):
    LOGGER.info(f"Handeling \"add_ticket_to_order\" request for order ID: {order_id}")
    LOGGER.debug(f"Ticket data received: {ticket}, type: {type(ticket)}")

    order = helper_functions.get_order_by_id(order_id)
    if order is None:
        LOGGER.error(f"Order with ID {order_id} not found.")
        return {"error": f"Order with ID {order_id} not found."}

    order.get_tickets().append(ticket)

    FILEWRITERS["JSON_statefiles/orders.json"].remove_order_by_id(order_id)
    FILEWRITERS["JSON_statefiles/orders.json"].add_order(order)
    return {"message": f"Ticket with ID {ticket.get_ticket_id()} added to order with ID {order_id}."}

@back_end.post("/add_pending_ticket")
def add_pending_ticket(ticket: Ticket):
    LOGGER.info(f"Handeling \"add_pending_ticket\" request for ticket ID: {ticket.get_ticket_id()}")
    LOGGER.debug(f"Ticket data received: {ticket}, type: {type(ticket)}")
    FILEWRITERS["JSON_statefiles/pending_tickets.json"].add_ticket(ticket)
    return {"message": f"Ticket with ID {ticket.get_ticket_id()} added to pending tickets."}

@back_end.get("/get_all_pending_tickets_by_destination")
def get_all_pending_tickets_by_destination(destination: Destination):
    LOGGER.info(f"Handling \"get_all_pending_tickets_by_destination\" request for destination: {destination}")
    pending_tickets = FILEWRITERS["JSON_statefiles/pending_tickets.json"].get_tickets_by_destination(destination)
    return [ticket.serialize() for ticket in pending_tickets]

@back_end.get("/get_pending_ticket_by_id")
def get_pending_ticket_by_id(ticket_id: int):
    LOGGER.info(f"Handling \"get_pending_ticket_by_id\" request for ticket ID: {ticket_id}")
    ticket: Ticket | None = FILEWRITERS["JSON_statefiles/pending_tickets.json"].get_ticket_by_id(ticket_id)
    if ticket is None:
        LOGGER.error(f"Ticket with ID {ticket_id} not found in pending tickets.")
        return {"error": f"Ticket with ID {ticket_id} not found in pending tickets."}
    return ticket.serialize()

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

    if not (back_end_path / "JSON_statefiles" / "pending_tickets.json").is_file() or is_valid_json(back_end_path / "JSON_statefiles" / "pending_tickets.json") is False:
        LOGGER.info("pending_tickets.json file not found or corrupted. Creating a new one...")
        with open(back_end_path / "JSON_statefiles" / "pending_tickets.json", 'w') as f:
            json.dump([], f)

    if not (back_end_path / "JSON_backup" / "finished_orders.json").is_file() or is_valid_json(back_end_path / "JSON_backup" / "finished_orders.json") is False:
        LOGGER.info("finished_orders.json file not found or corrupted. Creating a new one...")
        with open(back_end_path / "JSON_backup" / "finished_orders.json", 'w') as f:
            json.dump([], f)

    LOGGER.info("All components initialized successfully. Back-end REST API is ready to handle requests.")
    return

@back_end.on_event("shutdown")
def shutdown_event():
    LOGGER.info("Shutting down the back_end REST API...")
    LOGGER.info("NEED TO IMPLEMENT BACKUP ON SHUTDOWN...")
    return