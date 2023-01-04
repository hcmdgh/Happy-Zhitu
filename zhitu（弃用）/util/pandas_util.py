import pandas as pd 

__all__ = [
    'read_csv', 
]


def read_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str)
    df = df.where(pd.notnull(df), None)

    return df 
