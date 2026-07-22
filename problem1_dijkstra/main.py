"""Console program for Dijkstra's shortest-path algorithm.

The core algorithm is implemented manually without a graph library.
An adjacency matrix uses None to mean that no edge exists.
"""

INFINITY = float("inf")


def dijkstra(graph, start):
    """Return shortest distances and predecessors from start."""
    vertex_count = len(graph)
    distances = [INFINITY] * vertex_count
    previous = [None] * vertex_count
    visited = [False] * vertex_count
    distances[start] = 0

    for _ in range(vertex_count):
        current = None
        smallest_distance = INFINITY

        # Greedy choice: manually find the nearest unvisited vertex.
        for vertex in range(vertex_count):
            if not visited[vertex] and distances[vertex] < smallest_distance:
                smallest_distance = distances[vertex]
                current = vertex

        if current is None:
            break

        visited[current] = True

        # Relax every valid outgoing edge.
        for neighbour in range(vertex_count):
            weight = graph[current][neighbour]
            if weight is None:
                continue
            if weight < 0:
                raise ValueError("Dijkstra's algorithm cannot use negative edges.")
            if visited[neighbour]:
                continue

            candidate = distances[current] + weight
            if candidate < distances[neighbour]:
                distances[neighbour] = candidate
                previous[neighbour] = current

    return distances, previous


def reconstruct_path(previous, start, destination):
    """Reconstruct one shortest path using the predecessor list."""
    path = []
    current = destination

    while current is not None:
        path.append(current)
        if current == start:
            break
        current = previous[current]

    if path[-1] != start:
        return []

    path.reverse()
    return path


def sample_data():
    names = ["A", "B", "C", "D", "E"]
    graph = [
        [0, 4, 2, None, None],
        [4, 0, 1, 5, None],
        [2, 1, 0, 8, 10],
        [None, 5, 8, 0, 2],
        [None, None, 10, 2, 0],
    ]
    return names, graph, 0


def read_integer(prompt, minimum, maximum=None):
    while True:
        try:
            value = int(input(prompt))
            if value < minimum or (maximum is not None and value > maximum):
                raise ValueError
            return value
        except ValueError:
            limit = f" to {maximum}" if maximum is not None else " or greater"
            print(f"Enter a whole number from {minimum}{limit}.")


def custom_data():
    count = read_integer("Number of vertices (2-20): ", 2, 20)
    names = []
    for index in range(count):
        name = input(f"Name of vertex {index + 1}: ").strip()
        names.append(name or f"V{index + 1}")

    graph = [[None for _ in range(count)] for _ in range(count)]
    for vertex in range(count):
        graph[vertex][vertex] = 0

    edge_count = read_integer("Number of undirected edges: ", 0)
    for edge_number in range(edge_count):
        print(f"Edge {edge_number + 1}")
        first = read_integer("  First vertex number: ", 1, count) - 1
        second = read_integer("  Second vertex number: ", 1, count) - 1
        weight = read_integer("  Non-negative weight: ", 0)
        graph[first][second] = weight
        graph[second][first] = weight

    start = read_integer("Starting vertex number: ", 1, count) - 1
    return names, graph, start


def display_results(names, distances, previous, start):
    print("\nSHORTEST-PATH RESULTS")
    print("-" * 55)
    print(f"{'Destination':<15}{'Distance':<12}Path")
    print("-" * 55)

    for destination, name in enumerate(names):
        path = reconstruct_path(previous, start, destination)
        if not path:
            print(f"{name:<15}{'Unreachable':<12}-")
            continue
        path_text = " -> ".join(names[vertex] for vertex in path)
        print(f"{name:<15}{distances[destination]:<12g}{path_text}")


def main():
    print("DIJKSTRA'S SHORTEST-PATH ALGORITHM")
    choice = input("Use sample data? (Y/n): ").strip().lower()
    names, graph, start = sample_data() if choice != "n" else custom_data()
    distances, previous = dijkstra(graph, start)
    display_results(names, distances, previous, start)


if __name__ == "__main__":
    main()

