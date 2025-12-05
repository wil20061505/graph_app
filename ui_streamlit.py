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

# ===============================
#  LƯU ĐỒ THỊ TRONG SESSION
# ===============================
if "graph" not in st.session_state:
    st.session_state.graph = Graph()

g = st.session_state.graph


st.title("Ứng dụng mô phỏng đồ thị")


# ===============================
#  NHẬP CẠNH
# ===============================
st.subheader("Thêm cạnh")
col1, col2, col3 = st.columns(3)
u = col1.text_input("Đỉnh U")
v = col2.text_input("Đỉnh V")
w = col3.number_input("Trọng số", min_value=1)

if st.button("Thêm cạnh"):
    if u and v:
        g.add_edge(u, v, w, undirected=True)          # >>> SỬA QUAN TRỌNG
        st.success("Đã thêm cạnh (vô hướng)")
    else:
        st.error("Vui lòng nhập đầy đủ U và V")


# ===============================
#  HIỂN THỊ ĐỒ THỊ
# ===============================
st.subheader("Đồ thị hiện tại")

G = nx.Graph()

# Thêm node
for node in g.adj:
    G.add_node(node)

# Thêm edge
for u in g.adj:
    for v, weight in g.adj[u].items():                # >>> SỬA LỖI ở đây
        G.add_edge(u, v, weight=weight)

# Vẽ đồ thị
fig, ax = plt.subplots()
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, ax=ax)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
st.pyplot(fig)


# ===============================
#  BFS / DFS
# ===============================
st.subheader("Duyệt đồ thị")
start = st.text_input("Điểm bắt đầu")
colA, colB = st.columns(2)

if colA.button("BFS"):
    st.write(bfs(g, start))

if colB.button("DFS"):
    st.write(dfs(g, start))


# ===============================
#  DIJKSTRA
# ===============================
st.subheader("Đường đi ngắn nhất")
target = st.text_input("Điểm kết thúc")
if st.button("Dijkstra"):
    dist, path = dijkstra(g, start, target)
    st.write("Đường đi:", path)
    st.write("Độ dài:", dist)


# ===============================
#  BIPARTITE
# ===============================
st.subheader("Kiểm tra đồ thị 2 phía")
if st.button("Kiểm tra bipartite"):
    st.write(is_bipartite(g))


# ===============================
#  MST
# ===============================
st.subheader("Cây bao trùm nhỏ nhất")
if st.button("Prim"):
    st.write(prim(g, start))

if st.button("Kruskal"):
    st.write(kruskal(g))


# ===============================
#  MAXFLOW
# ===============================
st.subheader("Ford–Fulkerson")
src = st.text_input("Nguồn")
sink = st.text_input("Đích")
if st.button("Maxflow"):
    st.write(ford_fulkerson(g, src, sink))


# ===============================
#  EULER
# ===============================
st.subheader("Chu trình Euler")
if st.button("Fleury"):
    st.write(fleury(g))

if st.button("Hierholzer"):
    st.write(hierholzer(g))
