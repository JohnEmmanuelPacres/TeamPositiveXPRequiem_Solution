import pandas as pd
import re
from thefuzz import process, fuzz
import streamlit as st

TARGET_SCHEMA = [
    "Teacher_ID", "Region", "Age", "Years_Experience", 
    "Educational_Attainment", "Major_Specialization", 
    "Subject_Taught", "Certification_Level", "Fragility_Indicator"
]

def clean_column_name(col: str) -> str:
    # Basic pre-cleaning string normalization
    col = re.sub(r'[^a-zA-Z0-9]', '_', col)
    return col.strip('_').title()

@st.cache_data
def normalize_dataframe_columns(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Uses fuzzy matching to map uploaded CSV columns to the DSS structural schema.
    Returns the corrected DataFrame.
    '''
    df_new = df.copy()
    raw_cols = df_new.columns.tolist()
    
    mapping = {}
    for raw in raw_cols:
        cleaned_raw = clean_column_name(raw)
        
        # Fuzzy match to TARGET_SCHEMA
        best_match, score = process.extractOne(cleaned_raw, TARGET_SCHEMA, scorer=fuzz.token_sort_ratio)
        
        # Set an arbitrary threshold to prevent catastrophic mapping
        if score > 50:
            mapping[raw] = best_match
        else:
            mapping[raw] = raw # Leave undefined columns as-is or drop them
            
    df_new.rename(columns=mapping, inplace=True)
    return df_new
