"""Console program for Dijkstra's shortest-path algorithm.

The algorithm is implemented manually without using a graph library.
The graph is represented using an adjacency matrix.

None means that no edge exists between two vertices.
"""

INFINITY = float("inf")


def dijkstra(graph, start, names):
    """Find shortest distances and paths from the starting vertex."""

    vertex_count = len(graph)

    # Initially, all vertices are assumed to be infinitely far away.
    distances = [INFINITY] * vertex_count

    # Stores the previous vertex used to reach each vertex.
    previous = [None] * vertex_count

    # Tracks whether a vertex's shortest distance has been finalized.
    visited = [False] * vertex_count

    # The distance from the starting vertex to itself is zero.
    distances[start] = 0

    print("\nGREEDY CHOICE AND DISTANCE UPDATES")
    print("=" * 75)

    stage = 1

    for _ in range(vertex_count):
        current = None
        smallest_distance = INFINITY

        # Greedy choice:
        # Find the unvisited vertex with the smallest known distance.
        for vertex in range(vertex_count):
            if not visited[vertex] and distances[vertex] < smallest_distance:
                smallest_distance = distances[vertex]
                current = vertex

        # Stop if no remaining vertex is reachable.
        if current is None:
            print("\nNo more reachable unvisited vertices.")
            break

        print(
            f"\nStage {stage}: Select vertex {names[current]} "
            f"because it has the smallest unvisited distance "
            f"({distances[current]:g})."
        )

        # The shortest distance to this vertex is now finalized.
        visited[current] = True
        update_made = False

        # Check every possible neighbour of the selected vertex.
        for neighbour in range(vertex_count):
            weight = graph[current][neighbour]

            # None means there is no edge.
            if weight is None:
                continue

            # Dijkstra's algorithm does not support negative edges.
            if weight < 0:
                raise ValueError(
                    "Dijkstra's algorithm cannot use negative edge weights."
                )

            # Do not update vertices whose distances are already finalized.
            if visited[neighbour]:
                continue

            # Calculate the distance through the current vertex.
            candidate = distances[current] + weight

            print(
                f"  Check {names[current]} -> {names[neighbour]}: "
                f"{distances[current]:g} + {weight:g} = {candidate:g}",
                end=""
            )

            # Relaxation:
            # Update the neighbour if the new path is shorter.
            if candidate < distances[neighbour]:
                old_distance = distances[neighbour]

                distances[neighbour] = candidate
                previous[neighbour] = current
                update_made = True

                if old_distance == INFINITY:
                    old_text = "infinity"
                else:
                    old_text = f"{old_distance:g}"

                print(
                    f" — update {names[neighbour]} "
                    f"from {old_text} to {candidate:g}."
                )
            else:
                print(" — no update; the existing route is shorter.")

        if not update_made:
            print("  No neighbour distances were improved.")

        stage += 1

    return distances, previous


def reconstruct_path(previous, start, destination):
    """Reconstruct one shortest path using the predecessor list."""

    path = []
    current = destination

    # Move backwards from the destination to the starting vertex.
    while current is not None:
        path.append(current)

        if current == start:
            break

        current = previous[current]

    # The destination is unreachable if the start was never reached.
    if not path or path[-1] != start:
        return []

    # Reverse the path so it goes from start to destination.
    path.reverse()

    return path


def sample_data():
    """Return a predefined sample graph."""

    names = ["A", "B", "C", "D", "E"]

    graph = [
        [0, 4, 2, None, None],
        [4, 0, 1, 5, None],
        [2, 1, 0, 8, 10],
        [None, 5, 8, 0, 2],
        [None, None, 10, 2, 0],
    ]

    # Start from vertex A.
    start = 0

    return names, graph, start


def read_integer(prompt, minimum, maximum=None):
    """Read and validate an integer entered by the user."""

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
                print(f"Enter a whole number of at least {minimum}.")
            else:
                print(
                    f"Enter a whole number from "
                    f"{minimum} to {maximum}."
                )


def custom_data():
    """Allow the user to enter a custom undirected graph."""

    count = read_integer(
        "Number of vertices (2-20): ",
        2,
        20
    )

    names = []

    print("\nENTER VERTEX NAMES")

    for index in range(count):
        name = input(
            f"Name of vertex {index + 1}: "
        ).strip()

        # Use a default name if the user enters nothing.
        if not name:
            name = f"V{index + 1}"

        names.append(name)

    # Create an adjacency matrix filled with None.
    graph = [
        [None for _ in range(count)]
        for _ in range(count)
    ]

    # The distance from a vertex to itself is zero.
    for vertex in range(count):
        graph[vertex][vertex] = 0

    print("\nVERTEX NUMBERS")

    for index, name in enumerate(names):
        print(f"{index + 1}. {name}")

    maximum_edges = count * (count - 1) // 2

    edge_count = read_integer(
        f"\nNumber of undirected edges "
        f"(0-{maximum_edges}): ",
        0,
        maximum_edges
    )

    entered_edges = set()

    for edge_number in range(edge_count):
        print(f"\nEdge {edge_number + 1}")

        while True:
            first = read_integer(
                "  First vertex number: ",
                1,
                count
            ) - 1

            second = read_integer(
                "  Second vertex number: ",
                1,
                count
            ) - 1

            if first == second:
                print(
                    "  An edge must connect two different vertices."
                )
                continue

            # Store the smaller number first so that A-B and B-A
            # are treated as the same undirected edge.
            edge_key = (min(first, second), max(first, second))

            if edge_key in entered_edges:
                print(
                    "  This edge has already been entered."
                )
                continue

            break

        weight = read_integer(
            "  Non-negative weight: ",
            0
        )

        # Store the edge in both directions.
        graph[first][second] = weight
        graph[second][first] = weight

        entered_edges.add(edge_key)

    start = read_integer(
        "\nStarting vertex number: ",
        1,
        count
    ) - 1

    return names, graph, start


def display_graph(names, graph):
    """Display the graph's adjacency matrix."""

    print("\nADJACENCY MATRIX")
    print("=" * 65)

    print(f"{'':<12}", end="")

    for name in names:
        print(f"{name:<10}", end="")

    print()

    for row, name in enumerate(names):
        print(f"{name:<12}", end="")

        for column in range(len(names)):
            value = graph[row][column]

            if value is None:
                text = "-"
            else:
                text = str(value)

            print(f"{text:<10}", end="")

        print()


def display_results(names, distances, previous, start):
    """Display the final shortest distances and paths."""

    print("\nFINAL SHORTEST-PATH RESULTS")
    print("=" * 70)

    print(
        f"{'Destination':<18}"
        f"{'Distance':<15}"
        f"Shortest Path"
    )

    print("-" * 70)

    for destination, name in enumerate(names):
        path = reconstruct_path(
            previous,
            start,
            destination
        )

        if not path:
            print(
                f"{name:<18}"
                f"{'Unreachable':<15}"
                f"-"
            )
            continue

        path_text = " -> ".join(
            names[vertex]
            for vertex in path
        )

        print(
            f"{name:<18}"
            f"{distances[destination]:<15g}"
            f"{path_text}"
        )


def main():
    """Run the complete console program."""

    print("=" * 55)
    print("DIJKSTRA'S SHORTEST-PATH ALGORITHM")
    print("=" * 55)

    choice = input(
        "Use sample data? (Y/n): "
    ).strip().lower()

    if choice == "n":
        names, graph, start = custom_data()
    else:
        names, graph, start = sample_data()

    display_graph(names, graph)

    print(
        f"\nStarting vertex: {names[start]}"
    )

    try:
        distances, previous = dijkstra(
            graph,
            start,
            names
        )

        display_results(
            names,
            distances,
            previous,
            start
        )

    except ValueError as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()