from pathlib import Path

import pandas as pd


def read_csv(filepath: str | Path) -> pd.DataFrame:
    df = pd.read_csv(filepath, dtype="str", na_filter=False)
    return df
