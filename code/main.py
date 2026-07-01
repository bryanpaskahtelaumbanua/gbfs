import time
import pandas as pd
import networkx as nx

from algoritma_gbfs import (
    get_node_from_location_name,
    get_itera_goal_node,
    greedy_best_first_search,
    calculate_total_distance,
    get_path_coordinates,
    nearest_node,
    ITERA_NAME
)

MAX_DISTANCE_TO_GRAPH = 5000  # meter


def build_graph_from_csv(nodes_file, edges_file):
    nodes = pd.read_csv(nodes_file)
    edges = pd.read_csv(edges_file)

    G = nx.DiGraph()

    for _, row in nodes.iterrows():
        G.add_node(
            int(row["node_id"]),
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"])
        )

    for _, row in edges.iterrows():
        G.add_edge(
            int(row["start_node"]),
            int(row["end_node"]),
            weight=float(row["length"])
        )

    return G


def get_start_location(G):
    while True:
        print("\n===== INPUT LOKASI AWAL =====")
        print("1. Masukkan nama lokasi")
        print("2. Masukkan koordinat manual")
        print("3. Kembali ke menu utama")

        choice = input("Pilih opsi: ")

        if choice == "1":
            location_name = input("Masukkan nama lokasi saat ini: ")

            start_node, start_lat, start_lon, start_distance = (
                get_node_from_location_name(G, location_name)
            )

            if start_node is None:
                print("\nLokasi tidak ditemukan atau tidak dapat dikenali.")
                print("Silakan coba nama lokasi yang lebih spesifik.")
                continue

            if start_distance > MAX_DISTANCE_TO_GRAPH:
                print("\nLokasi ditemukan, tetapi berada di luar cakupan dataset.")
                print("Jarak lokasi ke node terdekat:", round(start_distance, 2), "meter")
                print("Silakan coba nama lokasi lain atau gunakan koordinat manual.")
                continue

            return location_name, start_node, start_lat, start_lon, start_distance

        elif choice == "2":
            location_name = input("Masukkan nama lokasi saat ini: ")

            try:
                start_lat = float(input("Masukkan latitude : "))
                start_lon = float(input("Masukkan longitude: "))
            except ValueError:
                print("Koordinat tidak valid. Masukkan angka desimal.")
                continue

            if not (-90 <= start_lat <= 90):
                print("Latitude tidak valid. Nilai latitude harus antara -90 sampai 90.")
                continue

            if not (-180 <= start_lon <= 180):
                print("Longitude tidak valid. Nilai longitude harus antara -180 sampai 180.")
                continue

            start_node, start_distance = nearest_node(
                G,
                start_lat,
                start_lon
            )

            if start_node is None:
                print("Node terdekat tidak ditemukan.")
                continue

            if start_distance > MAX_DISTANCE_TO_GRAPH:
                print("\nKoordinat berada di luar cakupan dataset Lampung Selatan.")
                print("Jarak koordinat ke node terdekat:", round(start_distance, 2), "meter")
                continue

            return location_name, start_node, start_lat, start_lon, start_distance

        elif choice == "3":
            return None, None, None, None, None

        else:
            print("Pilihan tidak valid.")

def show_result(
    location_name,
    start_node,
    start_lat,
    start_lon,
    start_distance,
    goal_node,
    goal_distance,
    path,
    explored_nodes,
    total_distance,
    execution_time
):
    print("\n====================================")
    print("HASIL PENCARIAN RUTE")
    print("====================================")
    print("Lokasi Awal        :", location_name)
    print("Lokasi Tujuan      :", ITERA_NAME)
    print("Koordinat Awal     :", start_lat, ",", start_lon)
    print("Start Node         :", start_node)
    print("Goal Node          :", goal_node)
    print("Jarak lokasi awal ke node terdekat:", round(start_distance, 2), "meter")
    print("Jarak ITERA ke node terdekat      :", round(goal_distance, 2), "meter")

    if path is None:
        print("Status             : Rute tidak ditemukan")
        return

    print("Status             : Rute ditemukan")
    print("Jumlah Node Path   :", len(path))
    print("Node Dieksplorasi  :", explored_nodes)
    print("Total Jarak        :", round(total_distance, 2), "meter")
    print("Total Jarak        :", round(total_distance / 1000, 3), "km")
    print("Waktu Eksekusi     :", round(execution_time, 6), "detik")

    print("\nPreview Path:")
    if len(path) <= 10:
        print(path)
    else:
        print(path[:5], "...", path[-5:])


def main():
    nodes_file = "lampung_selatan_nodes.csv"
    edges_file = "lampung_selatan_edges.csv"

    print("Memuat dataset dan membangun graph...")
    G = build_graph_from_csv(nodes_file, edges_file)

    print("Graph berhasil dibuat.")
    print("Jumlah node:", G.number_of_nodes())
    print("Jumlah edge:", G.number_of_edges())

    goal_node, goal_distance = get_itera_goal_node(G)

    while True:
        print("\n====================================")
        print("SISTEM PENCARIAN RUTE MENUJU ITERA")
        print("Greedy Best-First Search")
        print("====================================")
        print("1. Cari Rute ke ITERA")
        print("2. Keluar")

        choice = input("Pilih menu: ")

        if choice == "1":
            location_name, start_node, start_lat, start_lon, start_distance = get_start_location(G)

            if start_node is None:
                continue

            start_time = time.time()

            path, explored_nodes = greedy_best_first_search(
                G,
                start_node,
                goal_node
            )

            end_time = time.time()
            execution_time = end_time - start_time

            total_distance = calculate_total_distance(G, path)

            show_result(
                location_name=location_name,
                start_node=start_node,
                start_lat=start_lat,
                start_lon=start_lon,
                start_distance=start_distance,
                goal_node=goal_node,
                goal_distance=goal_distance,
                path=path,
                explored_nodes=explored_nodes,
                total_distance=total_distance,
                execution_time=execution_time
            )

            path_coordinates = get_path_coordinates(G, path)

        elif choice == "2":
            print("Program selesai.")
            break

        else:
            print("Pilihan tidak valid. Silakan pilih 1 atau 2.")


if __name__ == "__main__":
    main()