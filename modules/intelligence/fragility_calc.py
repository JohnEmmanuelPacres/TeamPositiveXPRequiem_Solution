import pandas as pd
import streamlit as st
from core.dataframe_schema import normalize_record_columns

def calculate_fragility_score(row, w1: float, w2: float, w3: float) -> float:
    '''
    Generates a 1-100 vulnerability score based on base heuristical data and weighted pillars.
    Higher score means more fragile teaching node.
    '''
    # 1. Capacity Penalty (w1) - Based on fragility indicator or base risk
    capacity_score = 50
    indicator = str(row.get("fragility_indicator", "")).lower()
    if indicator == 'high':
        capacity_score = 100
    elif indicator == 'low':
        capacity_score = 0
        
    # 2. Experience Penalty (w2)
    exp_score = 50
    exp = row.get("years_experience", 0)
    if exp < 3:
        exp_score = 100
    elif exp > 10:
        exp_score = 0
        
    # 3. Mismatch Penalty (w3) - Based on certification
    mismatch_score = 50
    cert = str(row.get("certification_level", "")).lower()
    if 'level 1' in cert:
        mismatch_score = 100
    elif 'level 3' in cert:
        mismatch_score = 0

    # Apply Weights
    final_score = (capacity_score * w1) + (exp_score * w2) + (mismatch_score * w3)
    return round(max(1, min(100, final_score)), 2)

BASE_W1 = 0.4 #capacity penalty
BASE_W2 = 0.3 #experience penalty
BASE_W3 = 0.3 #mismatch penalty

def validation_weights(w1: float, w2: float, w3: float):
    if abs((w1 + w2 + w3) - 1.0) > 1e-5:
        raise ValueError("Total weights required is 1.0!")
    if any(abs(w - b) > 0.10 for w, b in [(w1, BASE_W1), (w2, BASE_W2), (w3, BASE_W3)]):
        raise ValueError("Weights should be within 10% of the baseline values!")
    return True

@st.cache_data
def append_fragility_scores(df: pd.DataFrame, w1: float = BASE_W1, w2: float = BASE_W2, w3: float = BASE_W3) -> pd.DataFrame:
    validation_weights(w1, w2, w3)
    df_new = normalize_record_columns(df, include_legacy_aliases=True)
    df_new["calculated_fragility_score"] = df_new.apply(lambda row: calculate_fragility_score(row, w1, w2, w3), axis=1)
    return normalize_record_columns(df_new, include_legacy_aliases=True)
