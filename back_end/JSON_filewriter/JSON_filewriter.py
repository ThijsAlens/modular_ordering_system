from abc import ABC, abstractmethod
import json
import threading
from pathlib import Path

class JSON_Filewriter(ABC):
    """
    An abstract class for writing and reading JSON data to and from a file.
    """

    def __init__(self, file_path: str):
        try:
            with open(file_path, 'r') as file:
                pass
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return
        self._file_path: Path = Path(file_path)
        self._lock: threading.Lock = threading.Lock()


    def append_to_file(self, data: list[object], truncate: bool = False) -> None:
        """
        Writes JSON data to a file.
        
        Args:
            data (list[object]): The data that needs to be written to the file. Each object must have a serialize() method that returns a JSON-serializable dictionary.
            truncate (bool): If True, truncates the file before writing. Defaults to False.
        
        Returns:
            None
        """
        with self._lock:
            try:
                file_content = json.loads(self._file_path.read_text()) if not truncate else []
                file_content.extend([obj.serialize() for obj in data])
                json_data = json.dumps(file_content, indent=4)
                self._file_path.write_text(json_data)
            except json.JSONDecodeError:
                print("Data must be a valid JSON string.")
        return


    def read_everything_from_file(self, object_class: type) -> list[object] | object | None:
        """
        Reads JSON data from a file.
        
        Args:
            None

        Returns:
            str: The JSON data read from the file, or None if an error occurred.
        """
        
        with self._lock:
            try:
                json_data = json.loads(self._file_path.read_text())
                return [object_class.deserialize(item) for item in json_data]

            except (json.JSONDecodeError, FileNotFoundError):
                print(f"Error reading from file: {self._file_path}")
                return None