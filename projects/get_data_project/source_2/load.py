import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from projects.core.elt_core import LoadData

class LoadDataSource2(LoadData):
    def load(self, data):
        # Implement the loading logic for source 2
        print("Loading data from source 2")
        for item in data:
            print(f"Loaded item: {item}")