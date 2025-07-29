import pandas as pd

def normalize_signal(df: pd.DataFrame, signal_col: str, group_col: str, method: str = "zscore") -> pd.Series:
    """
    Normalize a signal column within each group of a sweep parameter.

    Args:
        df (pd.DataFrame): Full DataFrame containing signal and grouping column.
        signal_col (str): Column to normalize (e.g., 'Ch3_y').
        group_col (str): Column to group by (e.g., 'param').
        method (str): 'zscore' or 'minmax'.

    Returns:
        pd.Series: Normalized signal column.
    """
    if method == "zscore":
        return df.groupby(group_col)[signal_col].transform(lambda x: (x - x.mean()) / x.std(ddof=0))
    elif method == "minmax":
        return df.groupby(group_col)[signal_col].transform(lambda x: (x - x.min()) / (x.max() - x.min()))
    else:
        raise ValueError(f"Unknown normalization method: {method}")
