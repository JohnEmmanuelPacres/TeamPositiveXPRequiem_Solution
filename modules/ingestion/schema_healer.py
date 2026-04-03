import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util
import streamlit as st
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time
import re

# The DSS Gold Standard Schema
TARGET_SCHEMA = [
    "Teacher_ID", "Region", "Age", "Years_Experience", 
    "Educational_Attainment", "Major_Specialization", 
    "Subject_Taught", "Certification_Level", "Fragility_Indicator"
]

@st.cache_resource
def load_semantic_model():
    """
    Multilingual model: Understands Tagalog (Guro/Lugar) vs English.
    """
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# FIX: Changed return hint from (pd.DataFrame, dict) to tuple[pd.DataFrame, dict]
def ai_normalize_columns(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    model = load_semantic_model()
    raw_cols = df.columns.tolist()
    
    target_embeddings = model.encode(TARGET_SCHEMA, convert_to_tensor=True)
    mapping = {}
    
    for raw in raw_cols:
        # Clean text to assist AI (removes symbols/numbers)
        clean_text = re.sub(r'[^a-zA-Z\s]', ' ', str(raw)).strip().lower()
        
        raw_embedding = model.encode(clean_text, convert_to_tensor=True)
        cos_scores = util.cos_sim(raw_embedding, target_embeddings)[0]
        best_match_idx = torch.argmax(cos_scores).item()
        confidence = cos_scores[best_match_idx].item()

        # Threshold for conceptual matching
        if confidence > 0.38:
            matched_header = TARGET_SCHEMA[best_match_idx]
            mapping[raw] = matched_header

    df_clean = df.rename(columns=mapping)
    
    # Auto-fill missing critical columns to prevent KeyErrors in other modules
    for col in TARGET_SCHEMA:
        if col not in df_clean.columns:
            df_clean[col] = "Not Specified"
            
    return df_clean, mapping

def get_coordinates(df):
    """Bridge to the Geospatial Pillar"""
    geolocator = Nominatim(user_agent="positive_xp_requiem_dss")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.9)
    
    unique_regions = df['Region'].unique()
    coords_map = {}
    
    for loc in unique_regions:
        if loc == "Not Specified" or pd.isna(loc): 
            continue
        try:
            # We append Philippines to make geocoding much faster/accurate
            location = geocode(f"{loc}, Philippines")
            if location:
                coords_map[loc] = (location.latitude, location.longitude)
        except:
            continue
            
    # Map the coordinates back to the dataframe
    df['latitude'] = df['Region'].map(lambda x: coords_map.get(x, (12.8797, 121.7740))[0])
    df['longitude'] = df['Region'].map(lambda x: coords_map.get(x, (12.8797, 121.7740))[1])
    return df