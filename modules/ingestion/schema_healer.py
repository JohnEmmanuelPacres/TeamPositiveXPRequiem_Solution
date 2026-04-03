import pandas as pd
import torch
import re
from sentence_transformers import SentenceTransformer, util
import streamlit as st
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

TARGET_SCHEMA = [
    "Teacher_ID", "Region", "Age", "Years_Experience", 
    "Educational_Attainment", "Major_Specialization", 
    "Subject_Taught", "Certification_Level", "Fragility_Indicator"
]

@st.cache_resource
def load_semantic_model():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def get_content_score(series: pd.Series) -> dict:
    """Heuristic Analysis: Looks at actual cell values to 'guess' the column type."""
    scores = {col: 0.0 for col in TARGET_SCHEMA}
    # Get a sample of non-null values as strings
    sample = series.dropna().astype(str).head(20).tolist()
    if not sample: return scores

    combined_sample = " ".join(sample).lower()

    # 1. Pattern: Teacher_ID (e.g., 2026-STAR-0001)
    if any(re.search(r'STAR-\d+', s) for s in sample):
        scores["Teacher_ID"] += 2.0
    
    # 2. Pattern: Certification_Level (e.g., Level 1, Antas 2)
    if "level" in combined_sample or "antas" in combined_sample:
        scores["Certification_Level"] += 2.0

    # 3. Numeric Analysis: Age vs Experience
    numeric_vals = pd.to_numeric(series, errors='coerce').dropna()
    if not numeric_vals.empty:
        avg = numeric_vals.mean()
        if 20 <= avg <= 70: scores["Age"] += 1.5
        if 0 <= avg <= 45: scores["Years_Experience"] += 1.2
    
    # 4. Keyword Analysis: Specialization / Subject
    subject_keywords = ["math", "physics", "science", "biology", "chemistry", "agham", "pisika"]
    if any(kw in combined_sample for kw in subject_keywords):
        scores["Major_Specialization"] += 1.0
        scores["Subject_Taught"] += 1.0

    # 5. Region Analysis
    region_keywords = ["region", "ncr", "barmm", "luzon", "visayas", "mindanao"]
    if any(kw in combined_sample for kw in region_keywords) or any(re.search(r'Region\s+[I|V|X]+', s) for s in sample):
        scores["Region"] += 2.0

    return scores

def ai_normalize_columns(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    model = load_semantic_model()
    raw_cols = df.columns.tolist()
    target_embeddings = model.encode(TARGET_SCHEMA, convert_to_tensor=True)
    
    mapping = {}
    
    for raw_col in raw_cols:
        # --- PHASE 1: Header Similarity (AI) ---
        clean_header = re.sub(r'[^a-zA-Z\s]', ' ', str(raw_col)).strip().lower()
        header_emb = model.encode(clean_header, convert_to_tensor=True)
        cos_scores = util.cos_sim(header_emb, target_embeddings)[0]
        
        # --- PHASE 2: Content Analysis (Heuristics) ---
        content_scores = get_content_score(df[raw_col])
        
        # --- PHASE 3: Hybrid Decision ---
        final_scores = {}
        for i, target in enumerate(TARGET_SCHEMA):
            # Combine AI confidence (0.0 to 1.0) with Heuristic Score
            ai_conf = cos_scores[i].item()
            heur_conf = content_scores[target]
            final_scores[target] = ai_conf + heur_conf

        best_target = max(final_scores, key=final_scores.get)
        
        # Confidence Threshold: Must have at least a decent combined score
        if final_scores[best_target] > 0.5:
            mapping[raw_col] = best_target

    # Apply renames
    df_clean = df.rename(columns=mapping)
    
    # Auto-fill missing critical columns
    for col in TARGET_SCHEMA:
        if col not in df_clean.columns:
            df_clean[col] = "Not Specified"
            
    return df_clean, mapping

def get_coordinates(df):
    """Safe Geocoding"""
    geolocator = Nominatim(user_agent="positive_xp_requiem_dss")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.8)
    
    unique_regions = df['Region'].unique()
    coords_map = {}
    
    for loc in unique_regions:
        if loc == "Not Specified" or pd.isna(loc): continue
        try:
            location = geocode(f"{loc}, Philippines")
            if location:
                coords_map[loc] = (location.latitude, location.longitude)
        except: continue
            
    df['latitude'] = df['Region'].map(lambda x: coords_map.get(x, (12.8797, 121.7740))[0])
    df['longitude'] = df['Region'].map(lambda x: coords_map.get(x, (12.8797, 121.7740))[1])
    return df