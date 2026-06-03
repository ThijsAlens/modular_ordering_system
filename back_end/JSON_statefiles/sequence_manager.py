import json
from pathlib import Path

class Sequence_manager:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        if not self.file_path.is_file():
            self._initialize_file()

    def _initialize_file(self):
        with open(self.file_path, 'w') as f:
            json.dump({"last_order_id": -1, "last_ticket_id": -1}, f, indent=4)

    def get_next_order_id(self) -> int:
        return self._increment_and_save("last_order_id")

    def get_next_ticket_id(self) -> int:
        return self._increment_and_save("last_ticket_id")
    
    def clear_file(self):
        self._initialize_file()

    def _increment_and_save(self, key: str) -> int:
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        
        # 2. Increment
        data[key] += 1
        new_id = data[key]
        
        # 3. Save it back (Using your new atomic temp-file logic here is a great idea!)
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)
            
        return new_id