import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from projects.core.elt_core import LoadData
from pendulum import DateTime
from typing import Any

class LoadDataSource2(LoadData):
    def load_data(self, data: Any, exec_date: DateTime):
       
        print("Loading data from source 2")
        for item in data:
            print(f"Loaded item: {item}")