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
# KHỞI TẠO ĐỒ THỊ
# =======================================================
if "graph" not in st.session_state:
    st.session_state.graph = Graph()
g = st.session_state.graph

st.title("Ứng dụng mô phỏng đồ thị")


# =======================================================
# THÊM / XÓA CẠNH
# =======================================================
st.subheader("Quản lý cạnh")

col1, col2, col3 = st.columns(3)
u = col1.text_input("Đỉnh U")
v = col2.text_input("Đỉnh V")
w = col3.number_input("Trọng số", min_value=1, value=1)

col_add, col_del = st.columns(2)

with col_add:
    if st.button("Thêm cạnh"):
        if u and v:
            g.add_edge(u, v, w, undirected=True)
            st.success(f"Đã thêm cạnh {u} — {v}")
        else:
            st.error("Vui lòng nhập U và V")

with col_del:
    if st.button("Xóa cạnh"):
        if u and v:
            if g.has_edge(u, v):
                g.remove_edge(u, v, undirected=True)
                st.success(f"Đã xóa cạnh {u} — {v}")
            else:
                st.warning("Cạnh không tồn tại")
        else:
            st.error("Vui lòng nhập U và V")


# =======================================================
# HIỂN THỊ ĐỒ THỊ
# =======================================================
st.subheader("Đồ thị hiện tại")

G = nx.Graph()
for node in g.adj:
    G.add_node(node)
for u0 in g.adj:
    for v0, weight in g.adj[u0].items():
        G.add_edge(u0, v0, weight=weight)

fig, ax = plt.subplots()
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color="lightblue", ax=ax)
edge_labels = nx.get_edge_attributes(G, "weight")
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

NEED_START = {"BFS", "DFS", "Dijkstra", "Prim", "Ford–Fulkerson"}
NEED_TARGET = {"Dijkstra", "Ford–Fulkerson"}

start = None
target = None

if algorithm in NEED_START:
    start = st.text_input("Điểm bắt đầu")

if algorithm in NEED_TARGET:
    target = st.text_input("Điểm kết thúc / đích")


# =======================================================
# CHẠY THUẬT TOÁN
# =======================================================
if st.button("▶ Chạy thuật toán"):

    if algorithm in NEED_START and not start:
        st.error("Thuật toán này cần điểm bắt đầu")
        st.stop()

    if algorithm in NEED_TARGET and not target:
        st.error("Thuật toán này cần điểm kết thúc")
        st.stop()

    if algorithm == "BFS":
        result = bfs(g, start)

    elif algorithm == "DFS":
        result = dfs(g, start)

    elif algorithm == "Dijkstra":
        dist, path = dijkstra(g, start, target)
        result = {"distance": dist, "path": path}

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
