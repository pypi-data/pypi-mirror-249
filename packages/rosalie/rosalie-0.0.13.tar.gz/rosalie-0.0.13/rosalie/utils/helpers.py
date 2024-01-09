import os

import numpy as np
import pandas as pd


def read_sample_data():
    """
    Read data initially prepared for ML analsyis, then process as needed.
    """
    print("Reading data from GBQ...")
    query = """
    SELECT * 
    FROM just-data-warehouse.experimentation.cuped_customer_level_data
    LIMIT 100000
    """
    return pd.read_gbq(query, project_id="just-data-expenab-dev")
