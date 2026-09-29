import streamlit as st
import math
import heapq
import networkx as nx
import matplotlib.pyplot as plt
# import the necessary functions and variables from searchAlgos.py
from searchAlgos import (
    hospital_graph,
    locations,
    gbfs,
    a_star
)

# Streamlit GUI
#*******************#

# Set Page Config
st.set_page_config(
    page_title="Emergency Supply Robot - Informed Search",
    page_icon="🏥",
    layout="centered"
)

# write meaningful title and description for the app
st.title("🏥 Emergency Supply Robot: Informed Search Visualizer")
st.write(
    "A hospital robot must deliver an emergency medical supply through a network of "
    "corridors. Pick a start node, a goal node and a search algorithm, then run the "
    "search to see the path it finds highlighted on the graph.\n\n"
    "- **GBFS** expands the node with the smallest heuristic, f(n) = h(n)\n"
    "- **A\\*** expands the node with the smallest f(n) = g(n) + h(n)\n\n"
    "The heuristic h(n) is the Euclidean (straight-line) distance to the goal."
)

# define the nodes and their coordinates
nodes = list(hospital_graph.keys())

# create a selectbox for the user to choose the start and goal nodes
start = st.selectbox(
    "Select Initial Node",
    nodes,
    index=nodes.index("Pharmacy")
)

goal = st.selectbox(
    "Select Goal Node",
    nodes,
    index=nodes.index("Emergency_Ward")
)

# create a selectbox for the user to choose the search algorithm
algorithm = st.selectbox(
    "Select Search Algorithm",
    ["GBFS", "A*"]
)


if st.button("Run Search"):

    if algorithm == "GBFS":

        # run the GBFS algorithm with the selected start and goal nodes
        path, cost = gbfs(start, goal)
    else:

        # run the A* algorithm with the selected start and goal nodes
        path, cost = a_star(start, goal)

    if path is None:

        # display a error message indicating that no path was found
        st.error(
            f"No path found from {start} to {goal}. "
            "The corridors are one-way, so not every node can reach every other node."
        )

    else:

        # Visualize NetworkX graph

        G = nx.DiGraph()

        for node, neighbors in hospital_graph.items():

            for neighbor, weight in neighbors.items():

                G.add_edge(node, neighbor, weight=weight)

        pos = locations

        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        path_edges = list(zip(path, path[1:]))
        node_colors = [
            "tomato" if n == start else
            "gold" if n == goal else
            "lightgreen" if n in path else
            "lightsteelblue"
            for n in G.nodes()
        ]

        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,
                               node_size=2200, edgecolors="black")
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=9, font_weight="bold")
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color="gray", width=1.5,
                               arrows=True, arrowsize=20, node_size=2200)
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=path_edges, edge_color="red",
                               width=4, arrows=True, arrowsize=25, node_size=2200)
        nx.draw_networkx_edge_labels(G, pos, ax=ax,
                                     edge_labels=nx.get_edge_attributes(G, "weight"),
                                     font_size=10)

        ax.set_title(
            f"{algorithm} Solution Path"
        )

        ax.axis("off")

        st.pyplot(fig)

        # Display result (below the graph)
        st.subheader("Search Result")

        st.write(
            f"**Algorithm:** {algorithm}"
        )

        st.write(
            f"**Solution Path:** {' → '.join(path)}"
        )

        st.write(
            f"**Total Path Cost:** {cost:.2f}"
        )
