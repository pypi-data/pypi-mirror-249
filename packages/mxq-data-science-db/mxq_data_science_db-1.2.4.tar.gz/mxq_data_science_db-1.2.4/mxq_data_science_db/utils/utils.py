""" General functions
"""
from typing import Iterator

import pandas as pd


def split_dataframe(df: pd.DataFrame, chuck_size: int = 10**4) -> Iterator:
    """Split the dataframe in chunks

    Args:
        df (pd.DataFrame): DataFrame to be splited
        chuck_size (int, optional): rows size. Defaults to 10**4.

    Yields:
        Iterator: DataFrame chuck
    """
    num_chucks = len(df) // chuck_size + 1
    for i in range(num_chucks):
        yield df[i * chuck_size : (i + 1) * chuck_size]
