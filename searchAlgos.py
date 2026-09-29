import math
import heapq

# Graph, Use Case: Emergency Supply Robot

locations = {
    "Pharmacy": (0, 0),
    "Main_Corridor": (2, 1),
    "Patient_Wing": (1, 4),
    "Nursing_Station": (4, 2),
    "Laboratory": (5, 5),
    "Emergency_Ward": (8, 6)
}

hospital_graph = {
    "Pharmacy": {
        "Main_Corridor": 2.2,
        "Patient_Wing": 4.1
    },

    "Main_Corridor": {
        "Nursing_Station": 2.2
    },

    "Patient_Wing": {
        "Laboratory": 5.0
    },

    "Nursing_Station": {
        "Laboratory": 3.2,
        "Emergency_Ward": 6.0
    },

    "Laboratory": {
        "Emergency_Ward": 3.2
    },

    "Emergency_Ward": {}
}


# Heuristic: Euclidean distance between two locations
def heuristic(current, goal):
    x1, y1 = locations[current]
    x2, y2 = locations[goal]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Path reconstruction
def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def path_cost(path):
    return sum(hospital_graph[a][b] for a, b in zip(path, path[1:]))


# GBFS: f(n) = h(n)
def gbfs(start, goal):
    frontier = [(heuristic(start, goal), start)]
    came_from = {}
    visited = set()

    while frontier:
        _, current = heapq.heappop(frontier)

        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, path_cost(path)

        for neighbor in hospital_graph[current]:
            if neighbor not in visited and neighbor not in came_from and neighbor != start:
                came_from[neighbor] = current
                heapq.heappush(frontier, (heuristic(neighbor, goal), neighbor))

    return None, float("inf")


# A*: f(n) = g(n) + h(n)
def a_star(start, goal):
    frontier = [(heuristic(start, goal), 0.0, start)]
    came_from = {}
    g_cost = {start: 0.0}
    closed = set()

    while frontier:
        _, _, current = heapq.heappop(frontier)

        if current in closed:
            continue
        closed.add(current)

        if current == goal:
            return reconstruct_path(came_from, current), g_cost[current]

        for neighbor, cost in hospital_graph[current].items():
            new_g = g_cost[current] + cost
            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                came_from[neighbor] = current
                heapq.heappush(frontier, (new_g + heuristic(neighbor, goal), new_g, neighbor))

    return None, float("inf")
