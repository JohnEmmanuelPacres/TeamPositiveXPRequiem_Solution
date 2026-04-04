import pydeck as pdk
import pandas as pd
import streamlit as st
from core.dataframe_schema import normalize_record_columns

def create_heatmap_layer(df: pd.DataFrame) -> pdk.Layer:
    """
    Returns a hexagon density layer for the heatmap effect.
    """
    # Adding a vibrant color palette to make it look professional and appealing
    COLOR_RANGE = [
        [255, 255, 178],
        [254, 204, 92],
        [253, 141, 60],
        [240, 59, 32],
        [189, 0, 38],
    ]

    df = normalize_record_columns(df)
    return pdk.Layer(
        "HexagonLayer",
        data=df,
        get_position=["longitude", "latitude"],
        auto_highlight=True,
        radius=1500, # Reduced to 1.5km to ensure data points roughly stay inland
        elevation_scale=100, # Balanced elevation relative to normal radius
        pickable=True,
        elevation_range=[0, 3000],
        extrude=True,
        coverage=1,
        color_range=COLOR_RANGE,
    )

def create_scatter_layer(df: pd.DataFrame) -> pdk.Layer:
    """
    Plots individual teachers as points.
    """
    df = normalize_record_columns(df)
    return pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["longitude", "latitude"],
        get_color="[200, 30, 0, 160]",
        get_radius=200,
        pickable=True
    )

def create_arc_layer(df: pd.DataFrame) -> pdk.Layer:
    """
    Draws dynamic neon arcs simulating dispatch routing vectors.
    """
    df = normalize_record_columns(df)
    return pdk.Layer(
        "ArcLayer",
        data=df,
        get_width=6, # Thick glowing laser lines
        get_source_position=["source_lon", "source_lat"],
        get_target_position=["target_lon", "target_lat"],
        get_tilt=15, # Angular tilt for a cool 3D vaulting effect
        get_source_color=[0, 255, 128, 200], # Neon Green Origin
        get_target_color=[255, 0, 64, 255], # Red Impact Zone
        pickable=True,
        auto_highlight=True,
    )

def render_map(df: pd.DataFrame, view_state=None, arcs_df: pd.DataFrame=None):
    """
    Renders the pydeck map.
    """
    if view_state is None:
        # Changed max_zoom to 20 so users can zoom in close enough to see 3D buildings.
        view_state = pdk.ViewState(
            longitude=122.56, 
            latitude=12.2, 
            zoom=4.5, 
            min_zoom=4, 
            max_zoom=20, 
            pitch=45, 
            bearing=0
        )
    
    layers = [
        create_heatmap_layer(df),
        create_scatter_layer(df)
    ]
    
    if arcs_df is not None and not arcs_df.empty:
        layers.append(create_arc_layer(arcs_df))
    
    r = pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        tooltip={"html": "<b>Manpower Assessed:</b> {elevationValue} Teachers", "style": {"color": "white", "backgroundColor": "#222222"}},
        # Switch to "carto" so it works automatically without any API keys! 
        map_provider="carto", 
        # "voyager" style is Carto's equivalent to Google Maps (roads, labels, light background)
        map_style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
    )
    st.pydeck_chart(r)
