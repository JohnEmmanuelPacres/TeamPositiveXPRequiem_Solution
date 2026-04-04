import pandas as pd
import streamlit as st
from core.dataframe_schema import normalize_record_columns

def deploy_teacher(df: pd.DataFrame, teacher_id: str, new_region: str) -> pd.DataFrame:
    """
    Simulates sending a teacher to a new region to fix structural fragility.
    Modifies the in-memory dataframe and triggers a recalculation.
    """
    # Using df copied from session state
    work_df = normalize_record_columns(df, include_legacy_aliases=True)
    
    # Find the teacher
    idx = work_df.index[work_df["teacher_id"] == teacher_id].tolist()
    if idx:
        work_df.at[idx[0], "region"] = new_region
        
        # Re-map Latitude & Longitude based on the injection logic in data_loader
        from core.data_loader import REGION_COORDS
        new_lat = REGION_COORDS.get(new_region, (12.8797, 121.7740))[0]
        new_lon = REGION_COORDS.get(new_region, (12.8797, 121.7740))[1]
        
        work_df.at[idx[0], "latitude"] = new_lat
        work_df.at[idx[0], "longitude"] = new_lon
        
    return normalize_record_columns(work_df, include_legacy_aliases=True)
