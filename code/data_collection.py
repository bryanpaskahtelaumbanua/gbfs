import osmnx as ox

place = "Lampung Selatan, Lampung, Indonesia"

G_osm = ox.graph_from_place(
    place,
    network_type="drive",
    simplify=True
)

nodes, edges = ox.graph_to_gdfs(G_osm)

nodes = nodes.reset_index()
edges = edges.reset_index()

nodes_dataset = nodes[["osmid", "y", "x"]]
nodes_dataset.columns = ["node_id", "latitude", "longitude"]

edges_dataset = edges[["u", "v", "length"]]
edges_dataset.columns = ["start_node", "end_node", "length"]

nodes_dataset.to_csv("lampung_selatan_nodes.csv", index=False)
edges_dataset.to_csv("lampung_selatan_edges.csv", index=False)

print("Dataset berhasil dibuat")
print("Jumlah node:", len(nodes_dataset))
print("Jumlah edge:", len(edges_dataset))