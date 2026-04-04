import re
import pandas as pd

# Compatibility aliases used by existing views/engines.
LEGACY_COLUMN_ALIASES = {
    "teacher_id": "Teacher_ID",
    "first_name": "First_Name",
    "last_name": "Last_Name",
    "region": "Region",
    "age": "Age",
    "years_experience": "Years_Experience",
    "educational_attainment": "Educational_Attainment",
    "major_specialization": "Major_Specialization",
    "subject_taught": "Subject_Taught",
    "certification_level": "Certification_Level",
    "fragility_indicator": "Fragility_Indicator",
    "calculated_fragility_score": "Calculated_Fragility_Score",
    "cohort_cluster": "Cohort_Cluster",
    "cohort_name": "Cohort_Name",
    "distance_from_target": "Distance_from_target",
    "cluster": "Cluster",
    "latitude": "Latitude",
    "longitude": "Longitude",
    "source_lat": "Source_Lat",
    "source_lon": "Source_Lon",
    "target_lat": "Target_Lat",
    "target_lon": "Target_Lon",
}


def to_lower_snake(name: str) -> str:
    text = str(name).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return re.sub(r"_+", "_", text).strip("_")


def normalize_record_columns(df: pd.DataFrame, include_legacy_aliases: bool = True) -> pd.DataFrame:
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

    if include_legacy_aliases:
        for lower_col, legacy_col in LEGACY_COLUMN_ALIASES.items():
            if lower_col in normalized_df.columns and legacy_col not in normalized_df.columns:
                normalized_df[legacy_col] = normalized_df[lower_col]
            elif legacy_col in normalized_df.columns and lower_col not in normalized_df.columns:
                normalized_df[lower_col] = normalized_df[legacy_col]

    return normalized_df
