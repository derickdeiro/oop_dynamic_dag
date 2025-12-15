import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from projects.core.elt_core import LoadData
from pendulum import DateTime
from typing import Any

class LoadDataSource3(LoadData):
    def load(self, data: Any, exec_date: DateTime):
        # Implement the loading logic for source 3
        print("Loading data from source 3")
        for item in data:
            print(f"Loaded item: {item}")