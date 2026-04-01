import networkx as nx
from pyvis.network import Network
import pandas as pd
import tempfile

def build_pyvis_graph(df: pd.DataFrame, limit: int = 150) -> str:
    """
    Builds a PyVis HTML graph. 
    Limits nodes for performance to emulate an 'Obsidian-like' Neural Map.
    """
    work_df = df.head(min(limit, len(df)))
    
    G = nx.Graph()
    
    # Create Region Hubs
    regions = work_df["Region"].unique()
    for reg in regions:
        G.add_node(reg, size=30, color="#FF4B4B", title=f"Region Hub: {reg}")
        
    # Create Teacher Nodes
    for _, row in work_df.iterrows():
        t_id = row["Teacher_ID"]
        reg = row["Region"]
        subject = row["Major_Specialization"]
        
        # Color specific to subject for visual flair
        color_map = {
            "Physics": "#1E3A8A", # Blue
            "Chemistry": "#059669", # Green
            "Biology": "#D97706", # Orange
            "Mathematics": "#7C3AED", # Purple
            "General Science": "#6B7280" # Gray
        }
        node_color = color_map.get(subject, "#9CA3AF")
        
        G.add_node(t_id, size=15, color=node_color, title=f"{t_id} | {subject}")
        G.add_edge(reg, t_id, color="#374151")
        
    # PyVis Rendering
    net = Network(height="600px", width="100%", bgcolor="#0E1117", font_color="white")
    net.from_nx(G)
    
    # Physics settings to make it bouncy/springy like Obsidian
    net.toggle_physics(True)
    
    # Generate temporary HTML file string
    path = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    net.write_html(path.name)
    
    with open(path.name, 'r', encoding='utf-8') as f:
        html_data = f.read()
        
    return html_data
