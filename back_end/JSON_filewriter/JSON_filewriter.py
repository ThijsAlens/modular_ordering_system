from abc import ABC, abstractmethod
import json
import logging
import threading

class JSON_Filewriter(ABC):
    """
    An abstract class for writing and reading JSON data to and from a file.
    """

    def __init__(self, file_path: str):
        try:
            with open(file_path, 'r') as file:
                pass
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
            return
        self._file_path: str = file_path
        self._lock: threading.Lock = threading.Lock()

    
    def write_to_file(self, data: str, truncate: bool = False) -> None:
        """
        Writes JSON data to a file.
        
        Args:
            data (str): The JSON data to write to the file. Must be a valid JSON string.
            truncate (bool): If True, truncates the file before writing. Defaults to False.
        
        Returns:
            None
        """

        try:
            json.loads(data)
        except json.JSONDecodeError:
            logging.error("Data must be a valid JSON string.")
            return

        with self._lock:
            with open(self._file_path, 'r+') as file:
                if truncate:
                    file.truncate(0)
                file.write(data)
        return
    
    
    def read_from_file(self) -> str | None:
        """
        Reads JSON data from a file.
        
        Args:
            None

        Returns:
            str: The JSON data read from the file, or None if an error occurred.
        """
        
        with self._lock:
            with open(self._file_path, 'r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    logging.error(f"Error decoding JSON from file: {self._file_path}")
                    return None
        return data