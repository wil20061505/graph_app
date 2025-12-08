import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

from graph.graph_model import Graph
from graph.graph_bfs_dfs import bfs, dfs
from graph.graph_shortest_path import dijkstra
from graph.graph_bipartite import is_bipartite
from graph.graph_mst_prim import prim
from graph.graph_mst_kruskal import kruskal
from graph.graph_maxflow_ff import ford_fulkerson
from graph.graph_euler_fleury import fleury
from graph.graph_euler_hierholzer import hierholzer


# =======================================================
# KHỞI TẠO ĐỒ THỊ TRONG SESSION
# =======================================================
if "graph" not in st.session_state:
    st.session_state.graph = Graph()
g = st.session_state.graph


st.title("Ứng dụng mô phỏng đồ thị")


# =======================================================
# NHẬP CẠNH
# =======================================================
st.subheader("Thêm cạnh")
col1, col2, col3 = st.columns(3)
u = col1.text_input("Đỉnh U")
v = col2.text_input("Đỉnh V")
w = col3.number_input("Trọng số", min_value=1)

if st.button("Thêm cạnh"):
    if u and v:
        g.add_edge(u, v, w, undirected=True)
        st.success("Đã thêm cạnh")
    else:
        st.error("Vui lòng nhập U và V")


# =======================================================
# HIỂN THỊ ĐỒ THỊ
# =======================================================
st.subheader("Đồ thị hiện tại")

G = nx.Graph()
for node in g.adj:
    G.add_node(node)
for u in g.adj:
    for v, weight in g.adj[u].items():
        G.add_edge(u, v, weight=weight)

fig, ax = plt.subplots()
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, ax=ax)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
st.pyplot(fig)


# =======================================================
# CHỌN THUẬT TOÁN
# =======================================================
st.subheader("Chọn thuật toán")

algorithm = st.selectbox(
    "Thuật toán",
    [
        "BFS",
        "DFS",
        "Dijkstra",
        "Bipartite",
        "Prim",
        "Kruskal",
        "Ford–Fulkerson",
        "Euler Fleury",
        "Euler Hierholzer"
    ]
)

start = st.text_input("Điểm bắt đầu")
target = None
if algorithm in ["Dijkstra", "Ford–Fulkerson"]:
    target = st.text_input("Điểm kết thúc / đích")


# =======================================================
# CHẠY THUẬT TOÁN
# =======================================================
if st.button("Chạy thuật toán"):
    result = None

    if algorithm == "BFS":
        result = bfs(g, start)

    elif algorithm == "DFS":
        result = dfs(g, start)

    elif algorithm == "Dijkstra":
        dist, path = dijkstra(g, start, target)
        result = {"path": path, "distance": dist}

    elif algorithm == "Bipartite":
        result = is_bipartite(g)

    elif algorithm == "Prim":
        result = prim(g, start)

    elif algorithm == "Kruskal":
        result = kruskal(g)

    elif algorithm == "Ford–Fulkerson":
        result = ford_fulkerson(g, start, target)

    elif algorithm == "Euler Fleury":
        result = fleury(g)

    elif algorithm == "Euler Hierholzer":
        result = hierholzer(g)

    st.subheader("Kết quả")
    st.write(result)
