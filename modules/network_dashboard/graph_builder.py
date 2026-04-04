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
        
        is_legend = row["Years_Experience"] >= 15
        node_shape = "star" if is_legend else "dot"
        node_size = 25 if is_legend else 15
        
        # Enhanced Tooltip/Title for better UX
        years_exp = row["Years_Experience"]
        first_name = row.get("First_Name", "")
        last_name = row.get("Last_Name", "")
        prof_name = f"Prof. {first_name} {last_name}".strip() if first_name else "Unknown"
        
        label_title = f"{prof_name}\nID: {t_id}\n{subject}\n{years_exp} Yrs Exp"
        
        G.add_node(t_id, size=node_size, color=node_color, title=label_title, shape=node_shape)
        G.add_edge(reg, t_id, color="#374151")
        
    # PyVis Rendering
    net = Network(height="520px", width="100%", bgcolor="#0E1117", font_color="white", select_menu=True, filter_menu=False, cdn_resources="remote")
    net.from_nx(G)
    
    # Improved Physics settings and options for a premium feel
    net.set_options("""
    var options = {
      "nodes": {
        "borderWidthSelected": 3,
        "font": {
          "color": "#ffffff",
          "size": 14,
          "face": "Tahoma"
        },
        "shadow": {
          "enabled": true
        }
      },
      "edges": {
        "color": {
          "color": "#4a5568",
          "highlight": "#d1d5db"
        },
        "smooth": {
          "type": "continuous"
        }
      },
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -5000,
          "centralGravity": 0.3,
          "springLength": 95,
          "springConstant": 0.04,
          "damping": 0.09
        },
        "solver": "barnesHut",
        "stabilization": {
          "enabled": true,
          "iterations": 50,
          "updateInterval": 10,
          "onlyDynamicEdges": false,
          "fit": true
        }
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 200,
        "zoomView": true,
        "dragView": true
      }
    }
    """)
    
    # Generate temporary HTML file string
    path = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    net.write_html(path.name)
    
    with open(path.name, 'r', encoding='utf-8') as f:
        html_data = f.read()
        
    return html_data
