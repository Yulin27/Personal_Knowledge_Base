import pandas as pd
import psycopg2
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st
from src.database.postgres import Postgres

# Function to connect to the database
def fetch_data():
    postgres = Postgres()
    postgres.connect()
    query = """
    SELECT id, title, keywords, embedding, category, summary, text FROM knowledge_base;
    """
    df = pd.read_sql_query(query, postgres.conn)
    df["embedding"] = df["embedding"].apply(lambda x: list(map(float, x[1:-1].split(","))))
    postgres.close()
    return df

# Function to calculate similarity and build the graph
def create_graph(df, similarity_threshold=0.2):
    G = nx.Graph()
    category_colors = {
        "科技": "red",
        "旅游": "green",
        "生活": "blue",
        "default": "gray"
    }
    
    for _, row in df.iterrows():
        G.add_node(
            row["id"],
            title=row["title"],
            keywords=row["keywords"],
            category=row["category"],
            summary=row["summary"],
            text=row["text"],
            color=category_colors.get(row["category"], category_colors["default"])
        )
    
    for i, row1 in df.iterrows():
        for j, row2 in df.iterrows():
            if i < j:
                similarity = cosine_similarity([row1["embedding"]], [row2["embedding"]])[0][0]
                if similarity >= similarity_threshold:
                    G.add_edge(row1["id"], row2["id"], weight=similarity)
    
    return G

# Function to create a Plotly figure from the graph
def create_plotly_graph(G):
    pos = nx.spring_layout(G)
    node_x, node_y, node_colors, node_text = [], [], [], []
    edge_x, edge_y = [], []

    for node in G.nodes:
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_colors.append(G.nodes[node]["color"])
        node_text.append(
            f"ID: {node}<br>"
            f"<b>Title:</b> {G.nodes[node]['title']}<br>"
            f"<b>Keywords:</b> {', '.join(G.nodes[node]['keywords'])}<br>"
        )

    for edge in G.edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color="#888"), mode="lines"))
    fig.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        marker=dict(size=15, color=node_colors, line_width=2),
        text=node_text,
        hoverinfo="text"
    ))
    fig.update_layout(
        title="Knowledge Graph",
        showlegend=False,
        margin=dict(b=0, l=0, r=0, t=40),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False)
    )
    return fig

# Streamlit App
def main():
    st.title("Knowledge Graph Visualization")

    # Use a two-column layout
    col1, col2 = st.columns([1,1])  # Adjust the column widths if needed

    with col1:
        st.sidebar.header("Settings")
        similarity_threshold = st.sidebar.slider("Similarity Threshold", 0.0, 1.0, 0.2, 0.05)

        with st.spinner("Fetching data..."):
            df = fetch_data()
        

        with st.spinner("Building graph..."):
            G = create_graph(df, similarity_threshold)
        
        st.write("### Knowledge Graph")
        fig = create_plotly_graph(G)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write("### Node Details")
        selected_node = st.text_input("Enter a node ID to see details:")
        selected_node = int(selected_node) if selected_node else None
        if selected_node:
            node = G.nodes[selected_node]
            st.write(f"**Title:** {node['title']}")
            st.write(f"**Category:** {node['category']}")
            st.write(f"**Summary:** {node['summary']}")
            st.write(f"**Keywords:** {', '.join(node['keywords'])}")
            st.write(f"**Text:** {node['text']}")

        # Add a button to dismiss the node details view
        if st.button("Dismiss Details"):
            st.experimental_rerun()  # Refresh the page to clear the input

if __name__ == "__main__":
    main()
