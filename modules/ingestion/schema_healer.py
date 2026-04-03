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
    Switching to a MULTILINGUAL model.
    This model understands Tagalog, Cebuano, etc., and maps them to English concepts.
    """
    # This is ~420MB but much more powerful than the previous one
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def ai_normalize_columns(df: pd.DataFrame) -> (pd.DataFrame, dict):
    model = load_semantic_model()
    raw_cols = df.columns.tolist()
    
    # Pre-calculate embeddings for our target standard headers
    target_embeddings = model.encode(TARGET_SCHEMA, convert_to_tensor=True)
    mapping = {}
    
    for raw in raw_cols:
        # Clean the header string (remove numbers/symbols) to help the AI
        clean_text = re.sub(r'[^a-zA-Z\s]', ' ', raw).strip().lower()
        
        # AI creates a 'concept vector' for the messy header
        raw_embedding = model.encode(clean_text, convert_to_tensor=True)
        
        # Calculate how close this concept is to our 9 standard columns
        cos_scores = util.cos_sim(raw_embedding, target_embeddings)[0]
        best_match_idx = torch.argmax(cos_scores).item()
        confidence = cos_scores[best_match_idx].item()

        # If confidence > 0.4, it's usually a conceptual match
        if confidence > 0.4:
            matched_header = TARGET_SCHEMA[best_match_idx]
            mapping[raw] = matched_header

    # Apply the renaming
    df_clean = df.rename(columns=mapping)
    
    # Ensure critical columns exist even if not found (fills with 'Not Provided')
    for col in TARGET_SCHEMA:
        if col not in df_clean.columns:
            df_clean[col] = "Not Specified"
            
    return df_clean, mapping

def get_coordinates(df):
    """Bridge to the Geospatial Pillar"""
    geolocator = Nominatim(user_agent="positive_xp_requiem_dss")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.9)
    
    # Target only the column now correctly named 'Region'
    unique_regions = df['Region'].unique()
    coords_map = {}
    
    for loc in unique_regions:
        if loc == "Not Specified" or pd.isna(loc): continue
        try:
            location = geocode(f"{loc}, Philippines")
            if location:
                coords_map[loc] = (location.latitude, location.longitude)
        except:
            continue
            
    df['latitude'] = df['Region'].map(lambda x: coords_map.get(x, (12.8797, 121.7740))[0])
    df['longitude'] = df['Region'].map(lambda x: coords_map.get(x, (12.8797, 121.7740))[1])
    return df