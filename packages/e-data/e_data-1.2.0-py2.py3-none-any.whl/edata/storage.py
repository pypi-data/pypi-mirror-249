import os
import sqlite3
import pandas as pd
from .definitions import EdataData


def store(directory: str, data: EdataData):
    """Stores an EdataData element"""
    for item in data:
        _df = pd.DataFrame(data[item])
        if "datetime" in _df.columns:
            _df.set_index("datetime", inplace=True)

        _df.to_csv(os.path.join(directory, item + ".csv"))
