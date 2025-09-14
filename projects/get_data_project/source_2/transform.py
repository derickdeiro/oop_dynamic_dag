import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from projects.core.elt_core import TransformData

class TransformDataSource2(TransformData):
    def transform(self, data):
        # Implement the transformation logic for source 2
        print("Transforming data from source 2")
        # Example: convert all values to uppercase
        transformed_data = [{"id": item["id"], "value": item["value"].upper()} for item in data]
        return transformed_data