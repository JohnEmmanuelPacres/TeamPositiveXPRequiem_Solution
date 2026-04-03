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
    """Enhanced Heuristics for ultra-messy numeric data."""
    scores = {col: 0.0 for col in TARGET_SCHEMA}
    sample = series.dropna().astype(str).head(50).tolist()
    if not sample: return scores

    combined_sample = " ".join(sample).lower()

    # 1. ID Detection (Even if it's just a number)
    if series.is_unique and not pd.api.types.is_float_dtype(series):
        scores["Teacher_ID"] += 1.5 
    if any(re.search(r'STAR-\d+', s) for s in sample):
        scores["Teacher_ID"] += 3.0

    # 2. Certification Level (Handles "Level 1" or just "1")
    if "level" in combined_sample or "antas" in combined_sample:
        scores["Certification_Level"] += 2.0
    numeric_vals = pd.to_numeric(series, errors='coerce').dropna()
    if not numeric_vals.empty:
        if numeric_vals.max() <= 5 and numeric_vals.min() >= 1:
            scores["Certification_Level"] += 1.5 # Likely a Level 1-5 scale

    # 3. Age vs Experience
    if not numeric_vals.empty:
        avg = numeric_vals.mean()
        if 20 <= avg <= 70: scores["Age"] += 2.0
        if 0 <= avg <= 45: scores["Years_Experience"] += 1.8

    # 4. Subject/Specialization
    if any(kw in combined_sample for kw in ["math", "physics", "science", "biology", "pisika", "agham"]):
        scores["Major_Specialization"] += 1.2
        scores["Subject_Taught"] += 1.2

    # 5. Region
    if any(kw in combined_sample for kw in ["region", "ncr", "barmm", "luzon"]):
        scores["Region"] += 2.5

    return scores

def ai_normalize_columns(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    model = load_semantic_model()
    original_cols = df.columns.tolist()
    target_embeddings = model.encode(TARGET_SCHEMA, convert_to_tensor=True)
    
    mapping = {}
    used_targets = set()

    # PHASE 1: Identify Standard Columns
    for col in original_cols:
        # If already English and in Schema, keep it and mark as used
        if col in TARGET_SCHEMA:
            mapping[col] = col
            used_targets.add(col)
            continue

        # AI Header Check
        clean_header = re.sub(r'[^a-zA-Z\s]', ' ', str(col)).strip().lower()
        header_emb = model.encode(clean_header, convert_to_tensor=True)
        cos_scores = util.cos_sim(header_emb, target_embeddings)[0]
        
        # Content Check
        content_scores = get_content_score(df[col])
        
        # Combined Best Match
        best_score = -1
        best_fit = None
        
        for i, target in enumerate(TARGET_SCHEMA):
            if target in used_targets: continue # Prevent Duplicates
            
            score = cos_scores[i].item() + content_scores[target]
            if score > best_score:
                best_score = score
                best_fit = target

        if best_fit and best_score > 0.6: # Confidence Threshold
            mapping[col] = best_fit
            used_targets.add(best_fit)

    # PHASE 2: Handle Non-Schema Columns (Translate Tagalog to English)
    # This ensures "status ng guro" becomes "teacher status"
    for col in original_cols:
        if col not in mapping:
            clean_header = re.sub(r'[^a-zA-Z\s]', ' ', str(col)).strip().lower()
            # Find closest English words (Simple translation simulation)
            # In a hackathon, we assume any remaining Tagalog is "Other_Prop"
            mapping[col] = clean_header.replace(" ", "_").title()

    # PHASE 3: Execution & De-duplication
    df_clean = df.copy()
    df_clean.columns = [mapping.get(c, c) for c in df_clean.columns]
    
    # Remove any physical duplicates that might have slipped through
    df_clean = df_clean.loc[:, ~df_clean.columns.duplicated()].copy()

    # Ensure critical columns exist
    for col in TARGET_SCHEMA:
        if col not in df_clean.columns:
            df_clean[col] = "Not Specified"
            
    return df_clean, mapping

def get_coordinates(df):
    geolocator = Nominatim(user_agent="positive_xp_requiem_dss")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.8)
    unique_regions = df['Region'].unique()
    coords_map = {}
    for loc in unique_regions:
        if loc == "Not Specified" or pd.isna(loc): continue
        try:
            location = geocode(f"{loc}, Philippines")
            if location: coords_map[loc] = (location.latitude, location.longitude)
        except: continue
    df['latitude'] = df['Region'].map(lambda x: coords_map.get(x, (12.8797, 121.7740))[0])
    df['longitude'] = df['Region'].map(lambda x: coords_map.get(x, (12.8797, 121.7740))[1])
    return df