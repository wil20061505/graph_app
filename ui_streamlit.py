import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import time
from draw_graph import draw_graph_with_highlight

from graph.graph_model import Graph
from graph.graph_bfs_dfs import bfs, dfs , bfs_result, dfs_result
from graph.graph_shortest_path import dijkstra
from graph.graph_bipartite import is_bipartite
from graph.graph_mst_prim import prim
from graph.graph_mst_kruskal import kruskal
from graph.graph_maxflow_ff import ford_fulkerson
from graph.graph_euler_fleury import fleury
from graph.graph_euler_hierholzer import hierholzer


# Kiểm tra đỉnh có trong đô thị hay không.
def is_valid_vertex(g, v):
    return v and v in g.get_vertices()

def can_run(g, start=None, target=None):
    if start is not None and not is_valid_vertex(g, start):
        return False
    if target is not None and not is_valid_vertex(g, target):
        return False
    return True
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
placeholder = st.empty()

if algorithm in NEED_START:
    start = st.text_input("Điểm bắt đầu")

if algorithm in NEED_TARGET:
    target = st.text_input("Điểm kết thúc / đích")


# =======================================================
# CHẠY THUẬT TOÁN
# =======================================================
if start and start not in g.get_vertices():
    st.warning(f"Đỉnh '{start}' không tồn tại")

if target and target not in g.get_vertices():
    st.warning(f"Đỉnh '{target}' không tồn tại")

result = None

if algorithm == "BFS":
    if st.button("Chạy BFS", disabled=not can_run(g, start=start)):
        steps = bfs(g, start)

        for i, visited in enumerate(steps):
            fig = draw_graph_with_highlight(g, visited)
            placeholder.pyplot(fig)
            st.caption(f"Bước {i + 1}: đã thăm {list(visited)}")
            time.sleep(0.8)
        result = "Trực quan hóa thành công!"
elif algorithm == "DFS":
    if st.button("Chạy DFS", disabled=not can_run(g, start=start)):
        steps = dfs(g, start)

        for i, visited in enumerate(steps):
            fig = draw_graph_with_highlight(g, visited)
            placeholder.pyplot(fig)
            st.caption(f"Bước {i + 1}: đã thăm {list(visited)}")
            time.sleep(0.8)
        result = "Trực quan hóa thành công!"
elif algorithm == "Dijkstra":
    if st.button("Chạy Dijkstra", disabled=not can_run(g, start, target)):
        dist, path = dijkstra(g, start, target)
        result = {"Đường đi": path, "Khoảng cách": dist}

elif algorithm == "Bipartite":
    if st.button("Kiểm tra Bipartite"):
        if is_bipartite(g):
            result = "Đồ thị là đồ thị 2 phía "
        else:
            result = "Đồ thị không phải đồ thị 2 phía "

elif algorithm == "Prim":
    if st.button("Chạy Prim", disabled=not can_run(g, start=start)):
        result = prim(g, start)

elif algorithm == "Euler Fleury":
    if st.button("Chạy Fleury"):
        result = fleury(g)

elif algorithm == "Euler Hierholzer":
    if st.button("Chạy Hierholzer"):
        result = hierholzer(g)

elif algorithm == "Kruskal":
    st.subheader("Kruskal —  Cây khung nhỏ nhất (MST)")

    # --- Khởi tạo session state ---
    if "kr_steps" not in st.session_state:
        st.session_state.kr_steps = []
    if "kr_index" not in st.session_state:
        st.session_state.kr_index = 0
    if "kr_pos" not in st.session_state:
        st.session_state.kr_pos = None
    if "kr_total" not in st.session_state:
        st.session_state.kr_total = 0

    # --- Chạy Kruskal ---
    if st.button("Chạy Kruskal"):
        from graph.graph_mst_kruskal import kruskal

        mst_edges, steps, total_weight = kruskal(G)

        st.session_state.kr_steps = steps
        st.session_state.kr_index = 0
        st.session_state.kr_total = total_weight
        st.session_state.kr_pos = None  # reset layout

        st.success(f"MST chứa {len(mst_edges)} cạnh — Tổng trọng số = {total_weight}")

    # --- Không có steps ---
    steps = st.session_state.kr_steps
    idx = st.session_state.kr_index

    if len(steps) == 0:
        st.info("Chưa có bước nào. Nhấn 'Chạy Kruskal'.")
    else:

        # Giới hạn index
        idx = max(0, min(idx, len(steps) - 1))
        st.session_state.kr_index = idx

        step = steps[idx]

        st.markdown(f"## O Bước {idx+1}/{len(steps)}")
        st.write(step["description"])

        # Điều hướng bước trước / sau
        c1, _, c2 = st.columns([1, 4, 1])
        with c1:
            if st.button("◀", key="kr_prev"):
                st.session_state.kr_index = max(0, idx - 1)
        with c2:
            if st.button("▶", key="kr_next"):
                st.session_state.kr_index = min(len(steps) - 1, idx + 1)

        # LAYOUT cố định
        if st.session_state.kr_pos is None:
            # tạo layout cố định từ đồ thị ban đầu
            baseG = nx.Graph()
            for u in g.adj:
                for v in g.adj[u]:
                    baseG.add_edge(u, v)
            st.session_state.kr_pos = nx.spring_layout(baseG, seed=42)

        pos = st.session_state.kr_pos

        # hiện figure từ steps
        fig = step["fig"]
        st.pyplot(fig)

        # kết quả cuối
        if idx == len(steps) - 1:
            st.success(f"Tổng trọng số MST = {st.session_state.kr_total}")
            result=st.session_state.kr_total

# --- Ford–Fulkerson ----
elif algorithm == "Ford–Fulkerson":
    st.subheader("Ford–Fulkerson (Edmonds–Karp)")

    # Nhập nguồn và đích tách biệt, không bị reset
    src = start
    sink = target

    # Khởi tạo state cho FF nếu chưa có
    if "ff_steps" not in st.session_state:
        st.session_state.ff_steps = []
    if "ff_step_index" not in st.session_state:
        st.session_state.ff_step_index = 0
    if "ff_flow" not in st.session_state:
        st.session_state.ff_flow = 0
    if "ff_pos" not in st.session_state:
        st.session_state.ff_pos = None

    # Chạy thuật toán khi người dùng nhấn vào
    if st.button("Chạy Maxflow", disabled=not can_run(g, start, target)):
        if not src or not sink:
            st.error("Vui lòng nhập nguồn và đích!")
        else:
            flow, steps = ford_fulkerson(g, src, sink, record_steps=True) # pyright: ignore[reportGeneralTypeIssues]
            steps = steps or []
            st.session_state.ff_steps = steps
            st.session_state.ff_step_index = 0
            st.session_state.ff_flow = flow
            st.session_state.ff_pos = None
            if len(steps) == 0:
                st.info("Không có đường tăng — Maxflow = 0")
            else:
                st.success(f"Đã chạy xong! Maxflow = {flow}")

    # Chạy các bước nếu có
    steps = st.session_state.get("ff_steps") or []

    if len(steps) == 0:
        st.info("Chưa có bước nào để hiển thị. Nhấn 'Chạy Maxflow' để bắt đầu.")
        result = None
    else:
        # tạo index
        idx = int(st.session_state.get("ff_step_index", 0))
        idx = max(0, min(idx, len(steps) - 1))
        st.session_state.ff_step_index = idx
        step = steps[idx]

        st.markdown(f"## O Bước {idx + 1}/{len(steps)}")
        st.write(f"**Đường tăng:** {step['augment_path']}")
        st.write(f"**Bottleneck:** {step['bottleneck']}")
        st.write(f"**Flow tích lũy:** {step['flow_added']}")

        # Các nút điều hướng
        colA, colB, colC = st.columns([1, 2, 1])
        with colA:
            if st.button("◀", key="ff_prev"):
                st.session_state.ff_step_index = max(0, st.session_state.ff_step_index - 1)
        with colC:
            if st.button("▶", key="ff_next"):
                st.session_state.ff_step_index = min(len(steps) - 1, st.session_state.ff_step_index + 1)

        # Tạo các bước hiện ra
        residual = step["residual"]
        augment = step["augment_path"]
        orig_cap = {(u, v): w for u in g.adj for v, w in g.adj[u].items()}

        G_disp = nx.DiGraph()
        for node in g.get_vertices():
            G_disp.add_node(node)

        pairs = set(orig_cap.keys())
        for u in residual:
            for v, cap in residual[u].items():
                if cap > 0:
                    pairs.add((u, v))
        for u, v in augment:
            pairs.add((u, v))

        edge_labels = {}
        for (u, v) in pairs:
            cap = orig_cap.get((u, v), 0)
            flow_on = residual.get(v, {}).get(u, 0)
            G_disp.add_edge(u, v, flow=flow_on, cap=cap)
            edge_labels[(u, v)] = f"{flow_on}/{cap}"

        # layout
        # --- Layout cố định toàn bộ quá trình ---
        if st.session_state.ff_pos is None:
            # Tạo layout từ đồ thị gốc để không bị thay đổi theo residual
            base_G = nx.DiGraph()
            for u in g.adj:
                for v in g.adj[u]:
                    base_G.add_edge(u, v)
            st.session_state.ff_pos = nx.spring_layout(base_G, seed=42)

        pos = st.session_state.ff_pos

        # --- Vẽ các đường đi
        fig, ax = plt.subplots(figsize=(7, 5))

        # cạnh
        edgelist = list(G_disp.edges())
        # Build forward edges (where original capacity>0) and reverse edges (where flow>0 but cap may be 0)
        # Vẽ đường nối liên tiếp(khi trọng số >0) và ngược lại khi flow >0 hoặc 0
        forward_edges = []
        reverse_edges = []
        for (u, v) in edgelist:

            if (v, u) in G_disp.edges():

                if G_disp.edges[(u, v)].get('flow', 0) > 0 and G_disp.edges[(v, u)].get('flow', 0) == 0:
                    forward_edges.append((u, v))
                    reverse_edges.append((v, u))
                elif G_disp.edges[(v, u)].get('flow', 0) > 0 and G_disp.edges[(u, v)].get('flow', 0) == 0:
                    forward_edges.append((v, u))
                    reverse_edges.append((u, v))
                else:

                    forward_edges.append((u, v))
                    if (v, u) not in forward_edges:
                        reverse_edges.append((v, u))
            else:
                forward_edges.append((u, v))

        # Vẽ node và các flow
        nx.draw_networkx_nodes(G_disp, pos, ax=ax)
        nx.draw_networkx_labels(G_disp, pos, ax=ax)

        # 1) Vẽ đường đi
        if forward_edges:
            nx.draw_networkx_edges(
                G_disp,
                pos,
                edgelist=forward_edges,
                width=[2 if G_disp.edges[e]['flow'] > 0 else 1 for e in forward_edges],
                edge_color=["tab:blue" if G_disp.edges[e]['flow'] > 0 else "gray" for e in forward_edges],
                arrowstyle='-|>',
                arrowsize=12,
                ax=ax,
                connectionstyle="arc3,rad=0.0"
            )

        # 2) Vẽ đường ngược lại
        if reverse_edges:
            nx.draw_networkx_edges(
                G_disp,
                pos,
                edgelist=reverse_edges,
                width=[1.5 if G_disp.edges[e]['flow'] > 0 else 1 for e in reverse_edges],
                edge_color=["tab:orange" if G_disp.edges[e]['flow'] > 0 else "lightgray" for e in reverse_edges],
                arrowstyle='-|>',
                arrowsize=12,
                ax=ax,
                connectionstyle="arc3,rad=0.25"
            )

        # 3) Vẽ đường tăng flow
        augment_edges = []
        for e in augment:
            if e in G_disp.edges():
                augment_edges.append(e)
            else:
                augment_edges.append(e)

        if augment_edges:
            nx.draw_networkx_edges(
                G_disp,
                pos,
                edgelist=augment_edges,
                width=4,
                edge_color="red",
                arrowstyle='-|>',
                arrowsize=16,
                ax=ax,
                connectionstyle="arc3,rad=0.0"
            )

        # cạnh labels (flow/cap)
        nx.draw_networkx_edge_labels(G_disp, pos, edge_labels=edge_labels, ax=ax)

        ax.set_axis_off()
        st.pyplot(fig)

        # hiện thị kết quả
        result = st.session_state.ff_flow 
if algorithm == "BFS": 
    result = bfs_result(g,start)
elif algorithm == "DFS":
    result = dfs_result(g,start)  
st.subheader("Kết quả")
st.write(result)
