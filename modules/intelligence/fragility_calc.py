import pandas as pd

def calculate_fragility_score(row) -> int:
    '''
    Generates a 1-100 vulnerability score based on base heuristical data.
    Higher score means more fragile teaching node.
    '''
    score = 50
    
    # Penalize low experience
    if row["Years_Experience"] < 3:
        score += 30
    elif row["Years_Experience"] > 10:
        score -= 20
        
    # Reward higher certification
    cert = str(row["Certification_Level"]).lower()
    if 'level 3' in cert:
        score -= 25
    elif 'level 1' in cert:
        score += 15
        
    # Baseline modifier
    if str(row["Fragility_Indicator"]).lower() == 'high':
        score += 20
        
    return max(1, min(100, score))

def append_fragility_scores(df: pd.DataFrame) -> pd.DataFrame:
    df_new = df.copy()
    df_new["Calculated_Fragility_Score"] = df_new.apply(calculate_fragility_score, axis=1)
    return df_new
