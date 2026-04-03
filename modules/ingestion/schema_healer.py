import pandas as pd
import torch
import re
from sentence_transformers import SentenceTransformer, util
from transformers import MarianTokenizer, MarianMTModel
import streamlit as st
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

TARGET_SCHEMA = [
    "Teacher_ID", "Region", "Age", "Years_Experience", 
    "Educational_Attainment", "Major_Specialization", 
    "Subject_Taught", "Certification_Level", "Fragility_Indicator"
]

@st.cache_resource
def load_models():
    """Loads Multilingual Mapper and specific MarianMT Translator."""
    mapper = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    # Specific MarianMT classes are more stable than 'Auto' classes for this model
    model_name = "Helsinki-NLP/opus-mt-tl-en"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    
    return mapper, tokenizer, model

def translate_tagalog_to_english(text, tokenizer, model):
    """Translates text from Tagalog to English."""
    try:
        # Clean text: remove underscores and non-alpha for better translation
        clean_text = str(text).replace("_", " ").strip()
        inputs = tokenizer(clean_text.lower(), return_tensors="pt", padding=True)
        with torch.no_grad():
            translated = model.generate(**inputs)
        result = tokenizer.decode(translated[0], skip_special_tokens=True)
        return result if result else text
    except:
        return text

def get_content_score(series: pd.Series) -> dict:
    """Heuristic logic to identify messy IDs and Numbers."""
    scores = {col: 0.0 for col in TARGET_SCHEMA}
    if series.empty: return scores
    
    sample = series.dropna().astype(str).head(50).tolist()
    combined_sample = " ".join(sample).lower()

    # 1. ID Check: Is it highly unique? (Works for STAR-001 or just 1001)
    unique_ratio = series.nunique() / len(series) if len(series) > 0 else 0
    if unique_ratio > 0.95:
        scores["Teacher_ID"] += 2.5

    # 2. Numeric Range Logic
    numeric_vals = pd.to_numeric(series, errors='coerce').dropna()
    if not numeric_vals.empty:
        v_max = numeric_vals.max()
        v_avg = numeric_vals.mean()
        if 1 <= v_max <= 10: scores["Certification_Level"] += 2.0
        if 0 <= v_avg <= 50: scores["Years_Experience"] += 1.5
        if 20 <= v_avg <= 75: scores["Age"] += 2.0

    return scores

def ai_normalize_columns(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    mapper, tokenizer, model = load_models()
    original_cols = df.columns.tolist()
    target_embeddings = mapper.encode(TARGET_SCHEMA, convert_to_tensor=True)
    
    mapping = {}
    used_targets = set()

    # PHASE 1: Target Schema Mapping
    for col in original_cols:
        if col in TARGET_SCHEMA:
            mapping[col] = col
            used_targets.add(col)
            continue

        header_emb = mapper.encode(str(col).lower(), convert_to_tensor=True)
        cos_scores = util.cos_sim(header_emb, target_embeddings)[0]
        content_scores = get_content_score(df[col])
        
        best_score = -1
        best_fit = None
        
        for i, target in enumerate(TARGET_SCHEMA):
            if target in used_targets: continue
            score = cos_scores[i].item() + content_scores[target]
            if score > best_score:
                best_score = score
                best_fit = target

        if best_fit and best_score > 0.7:
            mapping[col] = best_fit
            used_targets.add(best_fit)

    # PHASE 2: Translation for Unknown Columns
    for col in original_cols:
        if col not in mapping:
            # Translate 'Status ng Guro' -> 'Teacher Status'
            eng_name = translate_tagalog_to_english(col, tokenizer, model)
            clean_name = eng_name.strip().title().replace(" ", "_")
            
            # Prevent Duplicate column names
            final_name = clean_name
            counter = 1
            while final_name in mapping.values():
                final_name = f"{clean_name}_{counter}"
                counter += 1
            mapping[col] = final_name

    # PHASE 3: Apply & Preserve All Rows
    df_clean = df.copy()
    df_clean.columns = [mapping.get(c, c) for c in df_clean.columns]
    
    # Safety De-duplication
    df_clean = df_clean.loc[:, ~df_clean.columns.duplicated()].copy()

    # Ensure critical columns exist for Map module
    for col in TARGET_SCHEMA:
        if col not in df_clean.columns:
            df_clean[col] = "Not Specified"
            
    return df_clean, mapping

def get_coordinates(df):
    """Bridge to Geospatial Pillar"""
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