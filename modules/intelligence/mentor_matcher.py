import pandas as pd
from core.dataframe_schema import normalize_record_columns

def find_mentors(df: pd.DataFrame, target_region: str, subject: str) -> pd.DataFrame:
    """
    Find 'Local Legends' in the same region, same subject, with high experience (> 15 yrs) 
    that can mentor newer teachers.
    """
    work_df = normalize_record_columns(df, include_legacy_aliases=True)
    mentors = work_df[
        (work_df["region"] == target_region) &
        (work_df["major_specialization"] == subject) &
        (work_df["years_experience"] >= 12)
    ]
    return mentors.sort_values(by="years_experience", ascending=False)
