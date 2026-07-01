import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

NODES_FILE = "lampung_selatan_nodes.csv"
EDGES_FILE = "lampung_selatan_edges.csv"

nodes = pd.read_csv(NODES_FILE)
edges = pd.read_csv(EDGES_FILE)

print("===== DATASET AWAL =====")
print("Jumlah node:", len(nodes))
print("Jumlah edge:", len(edges))

print("\n===== 5 DATA NODE PERTAMA =====")
print(nodes.head())

print("\n===== 5 DATA EDGE PERTAMA =====")
print(edges.head())

print("\n===== INFO KOLOM NODES =====")
nodes.info()

print("\n===== INFO KOLOM EDGES =====")
edges.info()

print("\n===== MISSING VALUE NODES =====")
print(nodes.isnull().sum())

print("\n===== MISSING VALUE EDGES =====")
print(edges.isnull().sum())

print("\n===== DUPLIKASI DATA =====")
print("Duplikat nodes:", nodes.duplicated().sum())
print("Duplikat edges:", edges.duplicated().sum())

print("\n===== STATISTIK LENGTH =====")
print(edges["length"].describe())

print("\nTotal panjang edge:", round(edges["length"].sum() / 1000, 2), "km")
print("Rata-rata length:", round(edges["length"].mean(), 2), "meter")
print("Edge terpendek:", round(edges["length"].min(), 2), "meter")
print("Edge terpanjang:", round(edges["length"].max(), 2), "meter")

print("\n===== PREPROCESSING =====")

nodes_clean = nodes[["node_id", "latitude", "longitude"]].copy()
edges_clean = edges[["start_node", "end_node", "length"]].copy()

nodes_clean = nodes_clean.dropna()
edges_clean = edges_clean.dropna()

nodes_clean = nodes_clean.drop_duplicates()
edges_clean = edges_clean.drop_duplicates()

nodes_clean["node_id"] = nodes_clean["node_id"].astype(int)
nodes_clean["latitude"] = nodes_clean["latitude"].astype(float)
nodes_clean["longitude"] = nodes_clean["longitude"].astype(float)

edges_clean["start_node"] = edges_clean["start_node"].astype(int)
edges_clean["end_node"] = edges_clean["end_node"].astype(int)
edges_clean["length"] = edges_clean["length"].astype(float)

edges_clean = edges_clean[edges_clean["length"] > 0]

valid_nodes = set(nodes_clean["node_id"])

edges_clean = edges_clean[
    edges_clean["start_node"].isin(valid_nodes)
    & edges_clean["end_node"].isin(valid_nodes)
]

print("Jumlah node setelah preprocessing:", len(nodes_clean))
print("Jumlah edge setelah preprocessing:", len(edges_clean))

print("\n===== 5 DATA NODE SETELAH PREPROCESSING =====")
print(nodes_clean.head())

print("\n===== 5 DATA EDGE SETELAH PREPROCESSING =====")
print(edges_clean.head())

G = nx.DiGraph()

for _, row in nodes_clean.iterrows():
    G.add_node(
        row["node_id"],
        latitude=row["latitude"],
        longitude=row["longitude"]
    )

for _, row in edges_clean.iterrows():
    G.add_edge(
        row["start_node"],
        row["end_node"],
        weight=row["length"]
    )

print("\n===== INFORMASI GRAPH =====")
print("Jumlah node graph:", G.number_of_nodes())
print("Jumlah edge graph:", G.number_of_edges())
print("Graph berarah:", nx.is_directed(G))

degree_values = [degree for _, degree in G.degree()]

print("\n===== DEGREE GRAPH =====")
print("Degree minimum:", min(degree_values))
print("Degree maksimum:", max(degree_values))
print("Rata-rata degree:", round(sum(degree_values) / len(degree_values), 2))

plt.figure(figsize=(8, 5))
plt.hist(edges_clean["length"], bins=50)
plt.title("Distribusi Panjang Edge Jalan")
plt.xlabel("Panjang Edge (meter)")
plt.ylabel("Frekuensi")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 5))
plt.hist(degree_values, bins=30)
plt.title("Distribusi Degree Node")
plt.xlabel("Degree")
plt.ylabel("Frekuensi")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 8))
plt.scatter(
    nodes_clean["longitude"],
    nodes_clean["latitude"],
    s=1
)
plt.title("Sebaran Node Jaringan Jalan Lampung Selatan")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.tight_layout()
plt.show()

summary = {
    "Jumlah Node Awal": len(nodes),
    "Jumlah Edge Awal": len(edges),
    "Jumlah Node Setelah Preprocessing": len(nodes_clean),
    "Jumlah Edge Setelah Preprocessing": len(edges_clean),
    "Jumlah Node Graph": G.number_of_nodes(),
    "Jumlah Edge Graph": G.number_of_edges(),
    "Total Panjang Edge (km)": round(edges_clean["length"].sum() / 1000, 2),
    "Rata-rata Length (m)": round(edges_clean["length"].mean(), 2),
    "Edge Terpendek (m)": round(edges_clean["length"].min(), 2),
    "Edge Terpanjang (m)": round(edges_clean["length"].max(), 2),
    "Degree Minimum": min(degree_values),
    "Degree Maksimum": max(degree_values),
    "Rata-rata Degree": round(sum(degree_values) / len(degree_values), 2)
}

print("\n===== RINGKASAN EDA & PREPROCESSING =====")
for key, value in summary.items():
    print(f"{key}: {value}")

print("\nEDA dan preprocessing selesai.")