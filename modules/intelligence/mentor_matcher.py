import pandas as pd

def find_mentors(df: pd.DataFrame, target_region: str, subject: str) -> pd.DataFrame:
    """
    Find 'Local Legends' in the same region, same subject, with high experience (> 15 yrs) 
    that can mentor newer teachers.
    """
    mentors = df[
        (df["Region"] == target_region) & 
        (df["Major_Specialization"] == subject) & 
        (df["Years_Experience"] >= 12)
    ]
    return mentors.sort_values(by="Years_Experience", ascending=False)
