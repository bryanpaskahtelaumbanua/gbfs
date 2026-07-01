import heapq
import osmnx as ox
from geopy.distance import geodesic

ITERA_NAME = "Institut Teknologi Sumatera, Lampung, Indonesia"

ITERA_LATITUDE = -5.357595571715167
ITERA_LONGITUDE = 105.31485682255209

def geocode_location(location_name):

    try:
        latitude, longitude = ox.geocode(location_name)
        return latitude, longitude

    except Exception as error:
        print("Geocoding gagal.")
        print("Detail error:", error)
        return None, None

def nearest_node(graph, latitude, longitude):

    nearest = None
    min_distance = float("inf")

    for node, data in graph.nodes(data=True):
        node_coord = (
            data["latitude"],
            data["longitude"]
        )

        target_coord = (
            latitude,
            longitude
        )

        distance = geodesic(target_coord, node_coord).meters

        if distance < min_distance:
            min_distance = distance
            nearest = node

    return nearest, min_distance

def get_node_from_location_name(graph, location_name):

    latitude, longitude = geocode_location(location_name)

    if latitude is None or longitude is None:
        return None, None, None, None

    node_id, distance_to_node = nearest_node(
        graph,
        latitude,
        longitude
    )

    return node_id, latitude, longitude, distance_to_node

def get_itera_goal_node(graph):

    goal_node, distance_to_node = nearest_node(
        graph,
        ITERA_LATITUDE,
        ITERA_LONGITUDE
    )

    return goal_node, distance_to_node

def heuristic(graph, current_node, goal_node):

    current_coord = (
        graph.nodes[current_node]["latitude"],
        graph.nodes[current_node]["longitude"]
    )

    goal_coord = (
        graph.nodes[goal_node]["latitude"],
        graph.nodes[goal_node]["longitude"]
    )

    return geodesic(current_coord, goal_coord).meters

def reconstruct_path(parent, goal_node):

    path = []
    current = goal_node

    while current is not None:
        path.append(current)
        current = parent[current]

    return path[::-1]

def greedy_best_first_search(graph, start_node, goal_node):
    priority_queue = []
    visited = set()
    parent = {}

    heapq.heappush(
        priority_queue,
        (heuristic(graph, start_node, goal_node), start_node)
    )

    parent[start_node] = None
    explored_count = 0

    while priority_queue:
        _, current_node = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)
        explored_count += 1

        if current_node == goal_node:
            path = reconstruct_path(parent, goal_node)
            return path, explored_count

        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:
                if neighbor not in parent:
                    parent[neighbor] = current_node

                neighbor_heuristic = heuristic(
                    graph,
                    neighbor,
                    goal_node
                )

                heapq.heappush(
                    priority_queue,
                    (neighbor_heuristic, neighbor)
                )

    return None, explored_count

def calculate_total_distance(graph, path):

    if path is None:
        return None

    total_distance = 0

    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]

        total_distance += graph[start][end]["weight"]

    return total_distance

def get_path_coordinates(graph, path):

    if path is None:
        return None

    coordinates = []

    for node in path:
        coordinates.append(
            (
                graph.nodes[node]["latitude"],
                graph.nodes[node]["longitude"]
            )
        )

    return coordinates