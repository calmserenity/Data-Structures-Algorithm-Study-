"""Kuala Lumpur shortest-path route planner using Dijkstra's algorithm."""

import math
from numbers import Real

INFINITY = float("inf")


def validate_graph(graph, start):
    """Validate an adjacency matrix and its starting vertex."""
    if not isinstance(graph, (list, tuple)) or len(graph) == 0:
        raise ValueError("The graph cannot be empty.")

    vertex_count = len(graph)

    if not isinstance(start, int) or isinstance(start, bool):
        raise ValueError("The starting location must be an integer index.")

    if start < 0 or start >= vertex_count:
        raise ValueError("The starting location is outside the graph.")

    for row in graph:
        if not isinstance(row, (list, tuple)) or len(row) != vertex_count:
            raise ValueError("The adjacency matrix must be square.")

    # Validate every edge before Dijkstra begins. This also checks edges in
    # disconnected parts of the graph.
    for row in graph:
        for weight in row:
            if weight is None:
                continue

            if not isinstance(weight, Real):
                raise ValueError("Edge weights must be numeric or None.")

            if not math.isfinite(weight):
                raise ValueError("Edge weights must be finite numbers.")

            if weight < 0:
                raise ValueError(
                    "Dijkstra's algorithm cannot use negative edge weights."
                )


def dijkstra(graph, start):
    """Return shortest distances and predecessors from the start vertex."""
    validate_graph(graph, start)

    vertex_count = len(graph)
    distances = [INFINITY] * vertex_count
    previous = [None] * vertex_count
    visited = [False] * vertex_count
    distances[start] = 0

    for _ in range(vertex_count):
        current = None
        smallest_distance = INFINITY

        # Greedy choice: manually select the nearest unvisited vertex.
        for vertex in range(vertex_count):
            if not visited[vertex] and distances[vertex] < smallest_distance:
                smallest_distance = distances[vertex]
                current = vertex

        # No reachable unvisited vertex remains.
        if current is None:
            break

        visited[current] = True

        # Relax every outgoing edge manually.
        for neighbour in range(vertex_count):
            weight = graph[current][neighbour]

            if weight is None or visited[neighbour]:
                continue

            candidate_distance = distances[current] + weight

            if candidate_distance < distances[neighbour]:
                distances[neighbour] = candidate_distance
                previous[neighbour] = current

    return distances, previous


def reconstruct_path(previous, start, destination):
    """Reconstruct one shortest path from start to destination."""
    if not isinstance(start, int) or not isinstance(destination, int):
        return []

    if isinstance(start, bool) or isinstance(destination, bool):
        return []

    if start < 0 or destination < 0:
        return []

    if start >= len(previous) or destination >= len(previous):
        return []

    path = []
    current = destination

    while current is not None:
        path.append(current)

        if current == start:
            break

        current = previous[current]

    if not path or path[-1] != start:
        return []

    path.reverse()
    return path


def kl_data():
    """Return the built-in Kuala Lumpur landmark network."""
    names = [
        "KL Sentral",
        "Pasar Seni",
        "Petaling Street",
        "Merdeka Square",
        "Masjid Jamek",
        "Bukit Bintang",
        "Pavilion KL",
        "KLCC",
        "TRX",
        "Mid Valley",
    ]

    graph = [
        [0, 2.0, None, 3.2, None, None, None, None, None, 4.0],
        [2.0, 0, 0.8, 1.4, 1.2, 3.0, None, None, None, None],
        [None, 0.8, 0, 1.5, 1.3, 2.6, None, None, None, None],
        [3.2, 1.4, 1.5, 0, 0.9, None, None, 3.8, None, None],
        [None, 1.2, 1.3, 0.9, 0, 2.8, None, 3.1, None, None],
        [None, 3.0, 2.6, None, 2.8, 0, 0.7, 2.0, 1.8, None],
        [None, None, None, None, None, 0.7, 0, 1.5, 1.6, None],
        [None, None, None, 3.8, 3.1, 2.0, 1.5, 0, 2.5, None],
        [None, None, None, None, None, 1.8, 1.6, 2.5, 0, 5.5],
        [4.0, None, None, None, None, None, None, None, 5.5, 0],
    ]

    return names, graph, 0


def read_integer(prompt, minimum, maximum=None):
    """Read a whole number within the requested range."""
    while True:
        try:
            value = int(input(prompt))

            if value < minimum:
                raise ValueError

            if maximum is not None and value > maximum:
                raise ValueError

            return value

        except ValueError:
            if maximum is None:
                print(f"Please enter a whole number of at least {minimum}.")
            else:
                print(
                    f"Please enter a whole number from {minimum} to {maximum}."
                )


def read_non_negative_number(prompt):
    """Read a finite, non-negative decimal number."""
    while True:
        try:
            value = float(input(prompt))

            if not math.isfinite(value) or value < 0:
                raise ValueError

            return value

        except ValueError:
            print("Please enter a finite, non-negative number.")


def display_locations(names):
    """Display all locations as a numbered menu."""
    print("\nAVAILABLE LOCATIONS")
    print("-" * 45)

    for index, name in enumerate(names, start=1):
        print(f"{index:>2}. {name}")

    print("-" * 45)


def select_location(names, prompt):
    """Ask the user to select a location."""
    return read_integer(prompt, 1, len(names)) - 1


def custom_data():
    """Allow the user to create a custom undirected graph."""
    print("\nCREATE A CUSTOM LOCATION NETWORK")
    print("-" * 45)

    count = read_integer("Number of locations (2-20): ", 2, 20)
    names = []

    for index in range(count):
        while True:
            name = input(f"Name of location {index + 1}: ").strip()

            if not name:
                print("The location name cannot be empty.")
                continue

            if name.lower() in (existing.lower() for existing in names):
                print("Each location must have a unique name.")
                continue

            names.append(name)
            break

    graph = [[None for _ in range(count)] for _ in range(count)]

    for vertex in range(count):
        graph[vertex][vertex] = 0

    maximum_edges = count * (count - 1) // 2
    edge_count = read_integer(
        f"Number of undirected routes (0-{maximum_edges}): ",
        0,
        maximum_edges,
    )

    added_edges = set()

    for edge_number in range(1, edge_count + 1):
        print(f"\nRoute {edge_number} of {edge_count}")
        display_locations(names)

        while True:
            first = select_location(names, "First location number: ")
            second = select_location(names, "Second location number: ")

            if first == second:
                print("A route must connect two different locations.")
                continue

            edge_key = tuple(sorted((first, second)))

            if edge_key in added_edges:
                print("That route already exists. Choose another pair.")
                continue

            break

        distance = read_non_negative_number(
            "Distance between the locations in kilometres: "
        )

        graph[first][second] = distance
        graph[second][first] = distance
        added_edges.add(edge_key)

    display_locations(names)
    start = select_location(names, "Choose the starting location: ")

    return names, graph, start


def format_distance(distance):
    """Format a distance value for display."""
    if math.isinf(distance):
        return "Unreachable"

    return f"{distance:.2f} km"


def display_single_route(names, distances, previous, start, destination):
    """Display the shortest route to one destination."""
    print("\n" + "=" * 62)
    print("KUALA LUMPUR SHORTEST ROUTE RESULT")
    print("=" * 62)
    print(f"Starting location : {names[start]}")
    print(f"Destination       : {names[destination]}")

    path = reconstruct_path(previous, start, destination)

    if not path:
        print("\nNo route exists between the selected locations.")
        print("=" * 62)
        return

    print("\nShortest route:")
    print(" -> ".join(names[vertex] for vertex in path))
    print(f"\nTotal distance: {format_distance(distances[destination])}")
    print("=" * 62)


def display_all_results(names, distances, previous, start):
    """Display shortest routes from the start to every destination."""
    print("\n" + "=" * 78)
    print(f"SHORTEST ROUTES FROM {names[start].upper()}")
    print("=" * 78)
    print(f"{'Destination':<20}{'Distance':<15}Route")
    print("-" * 78)

    for destination, name in enumerate(names):
        path = reconstruct_path(previous, start, destination)

        if not path:
            print(f"{name:<20}{'Unreachable':<15}-")
            continue

        path_text = " -> ".join(names[vertex] for vertex in path)
        distance_text = format_distance(distances[destination])
        print(f"{name:<20}{distance_text:<15}{path_text}")

    print("=" * 78)


def main():
    """Run the console application."""
    while True:
        print("\n" + "=" * 62)
        print("KUALA LUMPUR LANDMARK ROUTE PLANNER")
        print("Using Dijkstra's Shortest Path Algorithm")
        print("=" * 62)
        print("1. Use the Kuala Lumpur landmark data")
        print("2. Create a custom location network")
        print("3. Exit")

        choice = read_integer("\nChoose an option: ", 1, 3)

        if choice == 3:
            print("\nThank you for using the route planner. Goodbye!")
            break

        if choice == 1:
            names, graph, default_start = kl_data()
            display_locations(names)
            start = select_location(
                names,
                f"Choose the starting location [{default_start + 1}]: ",
            )
        else:
            names, graph, start = custom_data()

        while True:
            distances, previous = dijkstra(graph, start)

            print("\nRESULT DISPLAY OPTIONS")
            print("1. Show route to one destination")
            print("2. Show routes to every destination")

            display_choice = read_integer("Choose an option: ", 1, 2)

            if display_choice == 1:
                display_locations(names)
                destination = select_location(
                    names,
                    "Choose the destination: ",
                )
                display_single_route(
                    names,
                    distances,
                    previous,
                    start,
                    destination,
                )
            else:
                display_all_results(
                    names,
                    distances,
                    previous,
                    start,
                )

            print("\n" + "=" * 41)
            print("1. Find another destination")
            print("2. Change starting location")
            print("3. Return to main menu")
            print("4. Exit")

            option = read_integer("\nChoose option: ", 1, 4)

            if option == 1:
                continue

            if option == 2:
                display_locations(names)
                start = select_location(
                    names,
                    "Choose the new starting location: ",
                )
                continue

            if option == 3:
                break

            print("\nThank you for using the route planner. Goodbye!")
            return


if __name__ == "__main__":
    main()