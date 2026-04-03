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
    if 'Region' not in df.columns:
        return df
    
    geolocator = Nominatim(user_agent="positive_xp_requiem_dss")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    
    unique_regions = df['Region'].unique()
    coords_map = {}
    
    for loc in unique_regions:
        try:
            # We search within Philippines for better accuracy
            location = geocode(f"{loc}, Philippines")
            if location:
                coords_map[loc] = (location.latitude, location.longitude)
        except:
            continue
            
    df['latitude'] = df['Region'].map(lambda x: coords_map.get(x, (12.8797, 121.7740))[0])
    df['longitude'] = df['Region'].map(lambda x: coords_map.get(x, (12.8797, 121.7740))[1])
    return df

def ai_normalize_columns(df: pd.DataFrame) -> (pd.DataFrame, dict):
    model = load_semantic_model()
    raw_cols = df.columns.tolist()
    
    # 1. AI Semantic Mapping (Calculating Meaning)
    target_embeddings = model.encode(TARGET_SCHEMA, convert_to_tensor=True)
    mapping = {}
    
    for raw in raw_cols:
        raw_embedding = model.encode(raw, convert_to_tensor=True)
        # Compare messy column to all target columns
        cos_scores = util.cos_sim(raw_embedding, target_embeddings)[0]
        best_match_idx = torch.argmax(cos_scores).item()
        
        if cos_scores[best_match_idx] > 0.45: # Confidence threshold
            mapping[raw] = TARGET_SCHEMA[best_match_idx]
        else:
            # 2. Fallback to Fuzzy Matching if AI is unsure
            best_fuzzy, score = process.extractOne(raw, TARGET_SCHEMA, scorer=fuzz.token_sort_ratio)
            if score > 60:
                mapping[raw] = best_fuzzy

    df_clean = df.rename(columns=mapping)
    
    # Keep only standard columns + any lat/lng we might add
    valid_cols = [c for c in df_clean.columns if c in TARGET_SCHEMA]
    return df_clean[valid_cols], mapping