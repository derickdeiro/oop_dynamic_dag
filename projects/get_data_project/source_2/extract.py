import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from projects.core.elt_core import ExtractData
from pendulum import DateTime


class ExtractDataSource2(ExtractData):
    def extract_data(self, exec_date: DateTime):
       
        print("Extracting data from source 2")
       
        data = [{"id": 1, "value": "data1"}, {"id": 2, "value": "data2"}]
        return data