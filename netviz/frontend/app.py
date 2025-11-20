import streamlit as st
import requests
import time
import networkx as nx
import matplotlib.pyplot as plt

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="NetViz Dashboard", layout="wide")
st.title("🌐 NetViz - Network Visualization Dashboard")

placeholder_graph = st.empty()
placeholder_table = st.empty()

def fetch_devices():
    try:
        res = requests.get(f"{BACKEND_URL}/devices", timeout=5)
        if res.status_code == 200:
            return res.json()
        else:
            return []
    except Exception:
        return []

while True:
    devices = fetch_devices()

    if not devices:
        st.warning("No devices detected. Make sure backend is running.")
        time.sleep(5)
        st.experimental_rerun()

    # Build graph
    G = nx.Graph()
    G.add_node("Router", color="orange")

    for dev in devices:
        ip = dev["ip"]
        G.add_node(ip, color="skyblue")
        G.add_edge("Router", ip)

    # Draw graph
    fig, ax = plt.subplots(figsize=(6, 5))
    pos = nx.spring_layout(G, seed=42)
    colors = [G.nodes[n]["color"] for n in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=1200, font_size=8)
    
    placeholder_graph.pyplot(fig)

    # Show device table
    placeholder_table.subheader("Connected Devices")
    placeholder_table.table(devices)

    time.sleep(8)
    st.experimental_rerun()
