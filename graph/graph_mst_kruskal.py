import networkx as nx
import matplotlib.pyplot as plt

def kruskal(G):
    """
    Chạy thuật toán Kruskal và ghi lại từng bước để visual bằng Streamlit.

    Trả về:
        mst_edges  : danh sách cạnh trong MST
        steps      : danh sách bước cho visual
        total_weight: tổng trọng số cây khung nhỏ nhất
    """

    # --- Chuẩn bị ---
    edges = sorted(G.edges(data=True), key=lambda x: x[2].get("weight", 1))
    uf = {node: node for node in G.nodes()}

    def find(x):
        while uf[x] != x:
            x = uf[x]
        return x

    def union(a, b):
        uf[find(a)] = find(b)

    mst_edges = []
    steps = []

    # --- Layout giữ nguyên để tránh layout bị nhảy ---
    pos = nx.spring_layout(G, seed=42)

    # --- Bước 0: graph ban đầu ---
    fig, ax = plt.subplots(figsize=(6, 4))
    nx.draw(G, pos, with_labels=True, ax=ax)
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
    steps.append({
        "fig": fig,
        "description": "Khởi tạo – chưa chọn cạnh nào."
    })

    # --- Thuật toán Kruskal ---
    for u, v, data in edges:
        w = data.get("weight", 1)

        # snapshot trước khi quyết định chọn cạnh
        fig, ax = plt.subplots(figsize=(6, 4))
        nx.draw(G, pos, with_labels=True, ax=ax)

        nx.draw_networkx_edges(G, pos,
                               edgelist=[(u, v)],
                               width=3, edge_color="orange",
                               ax=ax)
        nx.draw_networkx_edge_labels(G, pos,
                                     edge_labels=nx.get_edge_attributes(G, "weight"),
                                     ax=ax)

        steps.append({
            "fig": fig,
            "description": f"Xét cạnh ({u}, {v}) trọng số {w}"
        })

        # kiểm tra có tạo cycle không
        if find(u) != find(v):
            union(u, v)
            mst_edges.append((u, v, w))

            # bước chọn cạnh
            fig, ax = plt.subplots(figsize=(6, 4))
            nx.draw(G, pos, with_labels=True, ax=ax)

            nx.draw_networkx_edges(G, pos,
                                   edgelist=mst_edges,
                                   width=3, edge_color="green",
                                   ax=ax)

            nx.draw_networkx_edge_labels(G, pos,
                                         edge_labels=nx.get_edge_attributes(G, "weight"),
                                         ax=ax)

            steps.append({
                "fig": fig,
                "description": f"Chọn cạnh ({u}, {v}) – thêm vào MST"
            })
        else:
            # bước loại cạnh vì tạo chu trình
            fig, ax = plt.subplots(figsize=(6, 4))
            nx.draw(G, pos, with_labels=True, ax=ax)

            nx.draw_networkx_edges(G, pos,
                                   edgelist=[(u, v)],
                                   width=3, edge_color="red",
                                   style="dashed",
                                   ax=ax)

            nx.draw_networkx_edge_labels(G, pos,
                                         edge_labels=nx.get_edge_attributes(G, "weight"),
                                         ax=ax)

            steps.append({
                "fig": fig,
                "description": f"Loại cạnh ({u}, {v}) – tạo chu trình"
            })

    # --- Tính tổng trọng số MST ---
    total_weight = sum(w for (_, _, w) in mst_edges)

    # --- Bước cuối: MST hoàn chỉnh ---
    fig, ax = plt.subplots(figsize=(6, 4))
    nx.draw(G, pos, with_labels=True, ax=ax)
    nx.draw_networkx_edges(G, pos,
                           edgelist=mst_edges,
                           width=3, edge_color="green",
                           ax=ax)

    nx.draw_networkx_edge_labels(G, pos,
                                 edge_labels=nx.get_edge_attributes(G, "weight"),
                                 ax=ax)

    steps.append({
        "fig": fig,
        "description": f"Hoàn thành! Tổng trọng số MST = {total_weight}"
    })

    return mst_edges, steps, total_weight
