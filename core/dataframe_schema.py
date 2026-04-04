import re
import pandas as pd


def to_lower_snake(name: str) -> str:
    text = str(name).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return re.sub(r"_+", "_", text).strip("_")


def normalize_record_columns(df: pd.DataFrame, include_legacy_aliases: bool = False) -> pd.DataFrame:
    """
    Normalize dataframe columns into lowercase snake_case.
    If duplicate logical columns are found (case/style variants), keep the first and
    backfill missing values from subsequent variants.
    """
    if df is None:
        return pd.DataFrame()

    normalized_data = {}
    for col in df.columns:
        normalized = to_lower_snake(col)
        series = df[col]
        if normalized in normalized_data:
            normalized_data[normalized] = normalized_data[normalized].combine_first(series)
        else:
            normalized_data[normalized] = series

    normalized_df = pd.DataFrame(normalized_data, index=df.index)

    return normalized_df
