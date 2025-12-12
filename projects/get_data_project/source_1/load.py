import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from projects.core.elt_core import LoadData
from typing import Any
from pendulum import DateTime

class LoadDataSource1(LoadData):
    def load(self, data: Any, exec_date: DateTime):
        # Implement the loading logic for source 1
        print("Loading data from source 1")
        for item in data:
            print(f"Loaded item: {item}")