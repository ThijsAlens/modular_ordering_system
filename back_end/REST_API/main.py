from fastapi import FastAPI
from pathlib import Path
import json
import logging

from back_end.REST_API.config import LOGGER

back_end = FastAPI()

@back_end.get("/")
def root():
    return {"message": "Welcome to the back_end REST API. Visit \"/docs\" for the API documentation."}

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