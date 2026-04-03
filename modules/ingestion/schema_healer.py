import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util
from thefuzz import process, fuzz
import streamlit as st
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

# EXACT SCHEMA expected by your Map and Analytics modules
TARGET_SCHEMA = [
    "Teacher_ID", "Region", "Age", "Years_Experience", 
    "Educational_Attainment", "Major_Specialization", 
    "Subject_Taught", "Certification_Level", "Fragility_Indicator"
]

@st.cache_resource
def load_semantic_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

def ai_normalize_columns(df: pd.DataFrame) -> (pd.DataFrame, dict):
    model = load_semantic_model()
    raw_cols = df.columns.tolist()
    
    target_embeddings = model.encode(TARGET_SCHEMA, convert_to_tensor=True)
    mapping = {}
    
    for raw in raw_cols:
        # Clean the string for better matching
        clean_raw = raw.replace('_', ' ').replace('-', ' ').strip()
        raw_embedding = model.encode(clean_raw, convert_to_tensor=True)
        
        cos_scores = util.cos_sim(raw_embedding, target_embeddings)[0]
        best_match_idx = torch.argmax(cos_scores).item()
        score = cos_scores[best_match_idx].item()
        
        # Lower threshold to 0.35 to be more inclusive
        if score > 0.35:
            mapping[raw] = TARGET_SCHEMA[best_match_idx]
        else:
            # Fallback to Fuzzy matching
            match, f_score = process.extractOne(clean_raw, TARGET_SCHEMA)
            if f_score > 60:
                mapping[raw] = match

    # Apply the renaming
    df_clean = df.rename(columns=mapping)
    
    # ENSURE CRITICAL COLUMNS EXIST (Empty if not found)
    for col in TARGET_SCHEMA:
        if col not in df_clean.columns:
            df_clean[col] = "Not Specified"

    return df_clean, mapping

def get_coordinates(df):
    """Free Geocoding for the Map"""
    geolocator = Nominatim(user_agent="positive_xp_requiem_dss")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.8)
    
    unique_regions = df['Region'].unique()
    coords_map = {}
    
    for loc in unique_regions:
        try:
            if loc == "Not Specified": continue
            location = geocode(f"{loc}, Philippines")
            if location:
                coords_map[loc] = (location.latitude, location.longitude)
        except:
            continue
            
    df['latitude'] = df['Region'].map(lambda x: coords_map.get(x, (12.8797, 121.7740))[0])
    df['longitude'] = df['Region'].map(lambda x: coords_map.get(x, (12.8797, 121.7740))[1])
    return df