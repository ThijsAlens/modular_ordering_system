# -- stuff to run tests from the test directory --
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# --------------------------------------------------

import json
from JSON_filewriter import JSON_Filewriter


class Test_Filewriter(JSON_Filewriter):
    def __init__(self, file_path: str):
        super().__init__(file_path)

class TestData:
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

    def serialize(self):
        return {
            'name': self.name,
            'value': self.value
        }

    @staticmethod
    def deserialize(data):
        return TestData(name=data['name'], value=data['value'])
    
if __name__ == "__main__":
    test = Test_Filewriter("test.json")
    data = TestData("example", 42)
    test.write_to_file(json.dumps(data.serialize(), indent=4), truncate=True)
    print(test.read_from_file())