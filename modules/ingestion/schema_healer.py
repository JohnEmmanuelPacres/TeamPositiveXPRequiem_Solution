import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util
from thefuzz import process, fuzz
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import streamlit as st
import time

# The "Gold Standard" we want every CSV to match
TARGET_SCHEMA = [
    "Teacher_ID", "Region", "Age", "Years_Experience", 
    "Educational_Attainment", "Major_Specialization", 
    "Subject_Taught", "Certification_Level", "Fragility_Indicator"
]

@st.cache_resource
def load_semantic_model():
    """Loads the Open-Source AI model (Approx 80MB)"""
    return SentenceTransformer('all-MiniLM-L6-v2')

def get_coordinates(df):
    """
    FREE GEOCODER: Converts 'Region' names to Lat/Lng.
    This bridges Feature 4 (Ingestion) with Feature 1 (Geospatial).
    """
    # If the AI renamed a column to 'Region', we use it. 
    # Otherwise, we look for anything that sounds like 'Region'
    region_col = None
    for col in df.columns:
        if col.lower() in ['region', 'lugar', 'location', 'province']:
            region_col = col
            break
            
    if not region_col:
        return df
    
    geolocator = Nominatim(user_agent="positive_xp_requiem_dss")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.8)
    
    # We only geocode UNIQUE regions to save time and API limits
    unique_regions = df[region_col].dropna().unique()
    coords_map = {}
    
    for loc in unique_regions:
        try:
            # Adding ", Philippines" makes it much more accurate
            location = geocode(f"{loc}, Philippines")
            if location:
                coords_map[loc] = (location.latitude, location.longitude)
        except:
            continue
            
    # Apply the coordinates back to the dataframe
    df['latitude'] = df[region_col].map(lambda x: coords_map.get(x, (12.8797, 121.7740))[0])
    df['longitude'] = df[region_col].map(lambda x: coords_map.get(x, (12.8797, 121.7740))[1])
    return df

def ai_normalize_columns(df: pd.DataFrame) -> (pd.DataFrame, dict):
    model = load_semantic_model()
    raw_cols = df.columns.tolist()
    
    target_embeddings = model.encode(TARGET_SCHEMA, convert_to_tensor=True)
    mapping = {}
    
    for raw in raw_cols:
        raw_embedding = model.encode(raw, convert_to_tensor=True)
        cos_scores = util.cos_sim(raw_embedding, target_embeddings)[0]
        best_match_idx = torch.argmax(cos_scores).item()
        
        # We only rename if we are 45% sure it matches a target
        if cos_scores[best_match_idx] > 0.45:
            mapping[raw] = TARGET_SCHEMA[best_match_idx]

    # RENAMING: This keeps ALL columns, but changes the names of the ones we found
    df_clean = df.rename(columns=mapping)
    
    return df_clean, mapping