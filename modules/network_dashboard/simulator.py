import pandas as pd
import streamlit as st

def deploy_teacher(df: pd.DataFrame, teacher_id: str, new_region: str) -> pd.DataFrame:
    """
    Simulates sending a teacher to a new region to fix structural fragility.
    Modifies the in-memory dataframe and triggers a recalculation.
    """
    # Using df copied from session state
    work_df = df.copy()
    
    # Find the teacher
    idx = work_df.index[work_df["Teacher_ID"] == teacher_id].tolist()
    if idx:
        work_df.at[idx[0], "Region"] = new_region
        
        # Re-map Latitude & Longitude based on the injection logic in data_loader
        from core.data_loader import REGION_COORDS
        new_lat = REGION_COORDS.get(new_region, (12.8797, 121.7740))[0]
        new_lon = REGION_COORDS.get(new_region, (12.8797, 121.7740))[1]
        
        work_df.at[idx[0], "Latitude"] = new_lat
        work_df.at[idx[0], "Longitude"] = new_lon
        
    return work_df
