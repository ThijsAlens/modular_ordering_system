

import json
from pathlib import Path
from sys import path

from back_end.JSON_filewriter.JSON_filewriter import JSON_Filewriter
from back_end.model.menu import Menu
from back_end.enums.destination import Destination


class Filewriter_menu(JSON_Filewriter):
    """
    A class for managing the "menu.json" state file.
    """

    def __init__(self, file_path: str):
        super().__init__(file_path)

    def load_menu_from_user_directory(self, dir_path: Path) -> None:
        """
        Loads the menu from a user-provided directory.

        Args:
            dir_path (Path): The path to the directory containing the JSON files with menu data.
        """
        for file in dir_path.iterdir():
            try:
                json.loads(file.read_text())
            except (json.JSONDecodeError, IsADirectoryError):
                print(f"Failed to decode JSON from the provided file {file}.")
                continue
            
            try:
                menu = Menu.deserialize(json.loads(file.read_text()))
            except json.JSONDecodeError:
                print(f"Failed to decode JSON from the provided file {file}.")
                return
            # except Exception as e:
            #     print(f"An error occurred while deserializing the menu from the provided file {file}: {e}")
            #     return
            
            self.append_to_file([menu], truncate=False)
        return
    
    def get_menu_by_destination(self, destination: Destination) -> Menu | None:
        """
        Retrieves the menu for a specific destination.

        Args:
            destination (Destination): The destination for which to retrieve the menu.
        Returns:
            Menu | None: The menu for the specified destination, or None if not found.
        """
        menus = self.read_everything_from_file(Menu)
        for menu in menus:
            if menu.destination == destination:
                return menu
        return None

