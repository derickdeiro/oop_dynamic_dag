import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from projects.core.elt_core import ExtractData
from pendulum import DateTime


class ExtractDataSource2(ExtractData):
    def extract(self, exec_date: DateTime):
        # Implement the extraction logic for source 2
        print("Extracting data from source 2")
        # Example: return data as a list of dictionaries
        data = [{"id": 1, "value": "data1"}, {"id": 2, "value": "data2"}]
        return data