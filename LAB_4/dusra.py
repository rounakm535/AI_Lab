import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import time

def bidirectional_bfs(graph, start, end):
    if start == end:
        return [start]
    
    # Frontiers
    front_start = {start}
    front_end = {end}
    
    # Parent trackers
    parent_start = {start: None}
    parent_end = {end: None}
    
    visited_start = set()
    visited_end = set()

    while front_start and front_end:
        # Expand from start
        new_front_start = set()
        for node in front_start:
            for neighbor in graph.neighbors(node):
                if neighbor not in visited_start:
                    parent_start[neighbor] = node
                    new_front_start.add(neighbor)
                    if neighbor in front_end:
                        return construct_path(parent_start, parent_end, neighbor)
        visited_start.update(front_start)
        front_start = new_front_start
        
        # Expand from end
        new_front_end = set()
        for node in front_end:
            for neighbor in graph.neighbors(node):
                if neighbor not in visited_end:
                    parent_end[neighbor] = node
                    new_front_end.add(neighbor)
                    if neighbor in front_start:
                        return construct_path(parent_start, parent_end, neighbor)
        visited_end.update(front_end)
        front_end = new_front_end
    
    return None  # No path found

def construct_path(parent_start, parent_end, meeting_point):
    path_start = []
    node = meeting_point
    while node:
        path_start.append(node)
        node = parent_start[node]
    path_end = []
    node = parent_end[meeting_point]
    while node:
        path_end.append(node)
        node = parent_end[node]
    return path_start[::-1] + path_end

def bfs(graph, start, end):
    queue = deque([(start, [start])])
    visited = set()
    while queue:
        current, path = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        for neighbor in graph.neighbors(current):
            if neighbor == end:
                return path + [neighbor]
            queue.append((neighbor, path + [neighbor]))
    return None

def dfs(graph, start, end, path=None, visited=None):
    if path is None:
        path = [start]
    if visited is None:
        visited = set()
    if start == end:
        return path
    visited.add(start)
    for neighbor in graph.neighbors(start):
        if neighbor not in visited:
            result = dfs(graph, neighbor, end, path + [neighbor], visited)
            if result:
                return result
    return None

def visualize_graph(graph, path, title="Graph"):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(8, 6))
    nx.draw(graph, pos, with_labels=True, node_color="lightblue", edge_color="gray")
    if path:
        edges_in_path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(graph, pos, edgelist=edges_in_path, edge_color="red", width=2)
    plt.title(title)
    plt.show()

# Create the graph
city_graph = nx.Graph()
city_graph.add_edges_from([
    ("A", "B"), ("A", "C"), ("B", "D"), ("C", "E"), 
    ("D", "E"), ("D", "F"), ("E", "F"), ("F", "G")
])

# Start and end nodes
start_node = "A"
end_node = "G"

# Compare methods
start_time = time.time()
bfs_path = bfs(city_graph, start_node, end_node)
print("BFS Path:", bfs_path, "Time:", time.time() - start_time)

start_time = time.time()
dfs_path = dfs(city_graph, start_node, end_node)
print("DFS Path:", dfs_path, "Time:", time.time() - start_time)

start_time = time.time()
bidirectional_path = bidirectional_bfs(city_graph, start_node, end_node)
print("Bi-directional BFS Path:", bidirectional_path, "Time:", time.time() - start_time)

# Visualize results
visualize_graph(city_graph, bfs_path, title="BFS Path")
visualize_graph(city_graph, dfs_path, title="DFS Path")
visualize_graph(city_graph, bidirectional_path, title="Bi-directional BFS Path")