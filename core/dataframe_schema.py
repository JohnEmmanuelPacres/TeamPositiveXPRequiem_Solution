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
    original_mappings = {}
    for col in df.columns:
        normalized = to_lower_snake(col)
        original_mappings[normalized] = col
        series = df[col]
        if normalized in normalized_data:
            normalized_data[normalized] = normalized_data[normalized].combine_first(series)
        else:
            normalized_data[normalized] = series

    normalized_df = pd.DataFrame(normalized_data, index=df.index)
    
    if include_legacy_aliases:
        # Add PascalCase legacy names that view.py expects
        pascal_mappings = {
            'cohort_name': 'Cohort_Name',
            'region': 'Region',
            'calculated_fragility_score': 'Calculated_Fragility_Score',
            'years_experience': 'Years_Experience',
            'age': 'Age',
            'subject_taught': 'Subject_Taught',
            'major_specialization': 'Major_Specialization',
            'teacher_id': 'Teacher_ID',
            'first_name': 'First_Name',
            'last_name': 'Last_Name',
            'educational_attainment': 'Educational_Attainment'
        }
        for snake_col, pascal_col in pascal_mappings.items():
            if snake_col in normalized_df.columns:
                normalized_df[pascal_col] = normalized_df[snake_col]

    return normalized_df
