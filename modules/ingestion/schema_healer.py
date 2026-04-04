import pandas as pd
import re
import streamlit as st
from core.dataframe_schema import normalize_record_columns

# Standard Lowercase Snake_Case Schema
TARGET_SCHEMA = [
    "teacher_id", "region", "age", "years_experience", 
    "educational_attainment", "major_specialization", 
    "subject_taught", "certification_level", "fragility_indicator"
]

# Manual override for common cross-language components to ensure accuracy
TAGALOG_MAP = {
    "guro": "teacher",
    "lugar": "region",
    "antas": "level",
    "sertipiko": "certification",
    "tinuturo": "taught",
    "tagal": "years",
    "serbisyo": "experience",
    "edad": "age"
}

@st.cache_resource
def load_models():
    from sentence_transformers import SentenceTransformer
    from transformers import MarianTokenizer, MarianMTModel
    mapper = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    model_name = "Helsinki-NLP/opus-mt-tl-en"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return mapper, tokenizer, model

def sanitize_column_name(name):
    """Converts names to lowercase_snake_case and fixes 'teachers' to 'teacher'."""
    name = str(name).lower()
    # Logic: Remove apostrophes and standardize "teachers" to "teacher"
    name = name.replace("'s", "").replace("’s", "").replace("teachers", "teacher")
    # Replace non-alphanumeric with underscore
    name = re.sub(r'[^a-z0-9]', '_', name)
    # Remove double underscores and trim
    name = re.sub(r'_+', '_', name).strip('_')
    return name

def translate_tagalog_to_english(text, tokenizer, model):
    import torch
    try:
        clean_text = str(text).replace("_", " ").strip()
        inputs = tokenizer(clean_text.lower(), return_tensors="pt", padding=True)
        with torch.no_grad():
            translated = model.generate(**inputs)
        return tokenizer.decode(translated[0], skip_special_tokens=True)
    except:
        return text

def ai_normalize_columns(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    import torch
    from sentence_transformers import util
    mapper, tokenizer, model = load_models()
    original_cols = df.columns.tolist()
    target_embeddings = mapper.encode(TARGET_SCHEMA, convert_to_tensor=True)
    
    mapping = {}
    used_targets = set()

    # --- STEP 1: KEYWORD & SEMANTIC MATCHING ---
    for col in original_cols:
        raw_low = str(col).lower()
        
        # 1.1 Direct keyword substitution (e.g., ID ng Guro -> id teacher)
        processed_header = raw_low
        for tg, en in TAGALOG_MAP.items():
            processed_header = processed_header.replace(tg, en)
        
        clean_processed = sanitize_column_name(processed_header)

        # 1.2 Check for exact match in target schema after substitution
        if clean_processed in TARGET_SCHEMA and clean_processed not in used_targets:
            mapping[col] = clean_processed
            used_targets.add(clean_processed)
            continue

        # 1.3 AI Semantic Check (High threshold for zero-intervention)
        header_emb = mapper.encode(clean_processed, convert_to_tensor=True)
        cos_scores = util.cos_sim(header_emb, target_embeddings)[0]
        best_match_idx = torch.argmax(cos_scores).item()
        
        if cos_scores[best_match_idx].item() > 0.50:
            target_field = TARGET_SCHEMA[best_match_idx]
            if target_field not in used_targets:
                mapping[col] = target_field
                used_targets.add(target_field)

    # --- STEP 2: TRANSLATE & SANITIZE REMAINING ---
    for col in original_cols:
        if col not in mapping:
            # e.g., "Status ng Guro" -> "Teacher Status"
            translated = translate_tagalog_to_english(col, tokenizer, model)
            clean_name = sanitize_column_name(translated)
            
            # De-duplicate names (e.g., teacher_status_1)
            final_name = clean_name
            counter = 1
            while final_name in mapping.values():
                final_name = f"{clean_name}_{counter}"
                counter += 1
            mapping[col] = final_name

    # --- STEP 3: APPLY TO DATAFRAME ---
    df_clean = df.copy()
    df_clean.columns = [mapping.get(c, c) for c in df_clean.columns]
    df_clean = df_clean.loc[:, ~df_clean.columns.duplicated()].copy()

    # Ensure critical columns exist for Map/Analytics
    for col in TARGET_SCHEMA:
        if col not in df_clean.columns:
            df_clean[col] = "not_specified"
            
    return df_clean, mapping

def get_coordinates(df):
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter
    geolocator = Nominatim(user_agent="positive_xp_requiem_dss")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.8)
    # Note: Using lowercase 'region' now
    unique_regions = df['region'].unique()
    coords_map = {}
    for loc in unique_regions:
        if loc == "not_specified" or pd.isna(loc): continue
        try:
            location = geocode(f"{loc}, Philippines")
            if location: coords_map[loc] = (location.latitude, location.longitude)
        except: continue
    df['latitude'] = df['region'].map(lambda x: coords_map.get(x, (12.8797, 121.7740))[0])
    df['longitude'] = df['region'].map(lambda x: coords_map.get(x, (12.8797, 121.7740))[1])
    return df