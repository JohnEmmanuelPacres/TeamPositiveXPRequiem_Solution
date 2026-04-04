import pandas as pd
from core.dataframe_schema import normalize_record_columns

def calculate_fragility_score(row) -> int:
    '''
    Generates a 1-100 vulnerability score based on base heuristical data.
    Higher score means more fragile teaching node.
    '''
    score = 50
    
    # Penalize low experience
    if row["years_experience"] < 3:
        score += 30
    elif row["years_experience"] > 10:
        score -= 20
        
    # Reward higher certification
    cert = str(row["certification_level"]).lower()
    if 'level 3' in cert:
        score -= 25
    elif 'level 1' in cert:
        score += 15
        
    # Baseline modifier
    if str(row["fragility_indicator"]).lower() == 'high':
        score += 20
        
    return max(1, min(100, score))

def append_fragility_scores(df: pd.DataFrame) -> pd.DataFrame:
    df_new = normalize_record_columns(df, include_legacy_aliases=True)
    df_new["calculated_fragility_score"] = df_new.apply(calculate_fragility_score, axis=1)
    return normalize_record_columns(df_new, include_legacy_aliases=True)
