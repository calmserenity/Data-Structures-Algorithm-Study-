"""Kuala Lumpur Landmark Route Planner using Dijkstra's algorithm."""

# A value used to represent a location that has not been reached yet.
INFINITY = float("inf")


def dijkstra(graph, start):
    """Return shortest distances and predecessors from the start vertex."""
    # The number of locations in the graph.
    vertex_count = len(graph)

    # The algorithm cannot run without any vertices.
    if vertex_count == 0:
        raise ValueError("The graph cannot be empty.")

    # Ensure the selected starting location exists.
    if start < 0 or start >= vertex_count:
        raise ValueError("The starting location is outside the graph.")

    # Every row must contain one value for every location.
    for row in graph:
        if len(row) != vertex_count:
            raise ValueError("The adjacency matrix must be square.")

    # Store the shortest known distance to each location.
    distances = [INFINITY] * vertex_count

    # Store the previous location used to reach each vertex.
    previous = [None] * vertex_count

    # Track which locations have already been processed.
    visited = [False] * vertex_count

    # The distance from the starting location to itself is zero.
    distances[start] = 0

    # Process at most one new vertex during each loop.
    for _ in range(vertex_count):
        current = None
        smallest_distance = INFINITY

        # Greedy choice: select the nearest unvisited location.
        for vertex in range(vertex_count):
            if not visited[vertex] and distances[vertex] < smallest_distance:
                smallest_distance = distances[vertex]
                current = vertex

        # Stop when no additional reachable vertex exists.
        if current is None:
            break

        # Mark the selected location as fully processed.
        visited[current] = True

        # Check every possible neighbour of the current location.
        for neighbour in range(vertex_count):
            weight = graph[current][neighbour]

            # None means there is no direct route between the locations.
            if weight is None:
                continue

            # Dijkstra's algorithm cannot correctly handle negative weights.
            if weight < 0:
                raise ValueError(
                    "Dijkstra's algorithm cannot use negative edge weights."
                )

            # A processed location does not need to be checked again.
            if visited[neighbour]:
                continue

            # Calculate the distance through the current location.
            candidate_distance = distances[current] + weight

            # Save the route only when it is shorter than the known route.
            if candidate_distance < distances[neighbour]:
                distances[neighbour] = candidate_distance
                previous[neighbour] = current

    return distances, previous


def reconstruct_path(previous, start, destination):
    """Reconstruct one shortest path from start to destination."""
    # Reject negative location indexes.
    if start < 0 or destination < 0:
        return []

    # Reject indexes that are outside the graph.
    if start >= len(previous) or destination >= len(previous):
        return []

    path = []
    current = destination

    # Trace backwards from the destination using previous vertices.
    while current is not None:
        path.append(current)

        # Stop once the starting location has been reached.
        if current == start:
            break

        current = previous[current]

    # An incomplete chain means that the destination is unreachable.
    if not path or path[-1] != start:
        return []

    # Reverse the path so it begins at the starting location.
    path.reverse()
    return path


def sample_data():
    """Return a built-in Kuala Lumpur landmark network.

    The distances are approximate demonstration values in kilometres.
    They are not intended to replace live navigation data.
    """
    # Each position in this list matches one row and column in the graph.
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

    # The adjacency matrix stores direct distances between locations.
    # None means that no direct route exists.
    graph = [
        # 0 KL Sentral
        [0, 2.0, None, 3.2, None, None, None, None, None, 4.0],

        # 1 Pasar Seni
        [2.0, 0, 0.8, 1.4, 1.2, 3.0, None, None, None, None],

        # 2 Petaling Street
        [None, 0.8, 0, 1.5, 1.3, 2.6, None, None, None, None],

        # 3 Merdeka Square
        [3.2, 1.4, 1.5, 0, 0.9, None, None, 3.8, None, None],

        # 4 Masjid Jamek
        [None, 1.2, 1.3, 0.9, 0, 2.8, None, 3.1, None, None],

        # 5 Bukit Bintang
        [None, 3.0, 2.6, None, 2.8, 0, 0.7, 2.0, 1.8, None],

        # 6 Pavilion KL
        [None, None, None, None, None, 0.7, 0, 1.5, 1.6, None],

        # 7 KLCC
        [None, None, None, 3.8, 3.1, 2.0, 1.5, 0, 2.5, None],

        # 8 TRX
        [None, None, None, None, None, 1.8, 1.6, 2.5, 0, 5.5],

        # 9 Mid Valley
        [4.0, None, None, None, None, None, None, None, 5.5, 0],
    ]

    # KL Sentral is the suggested starting location.
    default_start = 0
    return names, graph, default_start


def read_integer(prompt, minimum, maximum=None):
    """Read and validate a whole-number input."""
    while True:
        try:
            # Convert the user's input into an integer.
            value = int(input(prompt))

            # Reject values below the allowed range.
            if value < minimum:
                raise ValueError

            # Reject values above the allowed range when a maximum exists.
            if maximum is not None and value > maximum:
                raise ValueError

            return value

        except ValueError:
            # Display a suitable error message and ask again.
            if maximum is None:
                print(f"Please enter a whole number of at least {minimum}.")
            else:
                print(
                    f"Please enter a whole number from {minimum} to {maximum}."
                )


def read_non_negative_number(prompt):
    """Read and validate a non-negative decimal number."""
    while True:
        try:
            # Convert the user's input into a decimal number.
            value = float(input(prompt))

            # Route distances cannot be negative.
            if value < 0:
                raise ValueError

            return value

        except ValueError:
            print("Please enter a non-negative number.")


def display_locations(names):
    """Display all available locations as a numbered menu."""
    print("\nAVAILABLE LOCATIONS")
    print("-" * 45)

    # Number locations from 1 to make selection easier for the user.
    for index, name in enumerate(names, start=1):
        print(f"{index:>2}. {name}")

    print("-" * 45)


def select_location(names, prompt):
    """Ask the user to select one location from the menu."""
    # Convert the user's 1-based choice into a 0-based list index.
    return read_integer(prompt, 1, len(names)) - 1


def custom_data():
    """Allow the user to create a custom undirected location network."""
    print("\nCREATE A CUSTOM LOCATION NETWORK")
    print("-" * 45)

    # Limit the graph size to keep manual input manageable.
    count = read_integer("Number of locations (2-20): ", 2, 20)

    names = []

    # Read a unique name for every location.
    for index in range(count):
        while True:
            name = input(f"Name of location {index + 1}: ").strip()

            if not name:
                print("The location name cannot be empty.")
                continue

            # Compare names without considering uppercase or lowercase letters.
            if name.lower() in (existing.lower() for existing in names):
                print("Each location must have a unique name.")
                continue

            names.append(name)
            break

    # Create an empty adjacency matrix with no routes.
    graph = [[None for _ in range(count)] for _ in range(count)]

    # The distance from each location to itself is zero.
    for vertex in range(count):
        graph[vertex][vertex] = 0

    # Calculate the maximum possible routes in an undirected graph.
    maximum_edges = count * (count - 1) // 2
    edge_count = read_integer(
        f"Number of undirected routes (0-{maximum_edges}): ",
        0,
        maximum_edges,
    )

    # Store added pairs to prevent duplicate routes.
    added_edges = set()

    # Read the two endpoints and distance for every route.
    for edge_number in range(1, edge_count + 1):
        print(f"\nRoute {edge_number} of {edge_count}")
        display_locations(names)

        while True:
            first = select_location(names, "First location number: ")
            second = select_location(names, "Second location number: ")

            # A route must connect two separate locations.
            if first == second:
                print("A route must connect two different locations.")
                continue

            # Sort the pair so A-B and B-A are treated as the same route.
            edge_key = tuple(sorted((first, second)))

            if edge_key in added_edges:
                print("That route already exists. Choose another pair.")
                continue

            break

        distance = read_non_negative_number(
            "Distance between the locations in kilometres: "
        )

        # Save the distance in both directions because the graph is undirected.
        graph[first][second] = distance
        graph[second][first] = distance
        added_edges.add(edge_key)

    display_locations(names)
    start = select_location(names, "Choose the starting location: ")

    return names, graph, start


def format_distance(distance):
    """Format a distance value for display."""
    # Replace infinity with a clearer message for the user.
    if distance == INFINITY:
        return "Unreachable"

    # Display reachable distances with two decimal places.
    return f"{distance:.2f} km"


def display_single_route(names, distances, previous, start, destination):
    """Display the shortest route to one selected destination."""
    print("\n" + "=" * 62)
    print("KUALA LUMPUR SHORTEST ROUTE RESULT")
    print("=" * 62)

    print(f"Starting location : {names[start]}")
    print(f"Destination       : {names[destination]}")

    # Build the route from the predecessor information.
    path = reconstruct_path(previous, start, destination)

    # An empty path means the destination cannot be reached.
    if not path:
        print("\nNo route exists between the selected locations.")
        print("=" * 62)
        return

    # Convert vertex indexes into readable location names.
    print("\nShortest route:")
    print(" -> ".join(names[vertex] for vertex in path))
    print(f"\nTotal distance: {format_distance(distances[destination])}")
    print("=" * 62)


def display_all_results(names, distances, previous, start):
    """Display shortest routes from the start to every location."""
    print("\n" + "=" * 78)
    print(f"SHORTEST ROUTES FROM {names[start].upper()}")
    print("=" * 78)
    print(f"{'Destination':<20}{'Distance':<15}Route")
    print("-" * 78)

    # Reconstruct and display one route for every destination.
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

    # Keep displaying the main menu until the user exits.
    while True:
        # ==========================
        # Main Menu
        # ==========================
        print("\n" + "=" * 62)
        print("KUALA LUMPUR LANDMARK ROUTE PLANNER")
        print("Using Dijkstra's Shortest Path Algorithm")
        print("=" * 62)
        print("1. Use built-in Kuala Lumpur landmark data")
        print("2. Create a custom location network")
        print("3. Exit")

        choice = read_integer("\nChoose an option: ", 1, 3)

        # End the program when the user chooses Exit.
        if choice == 3:
            print("\nThank you for using the Kuala Lumpur Landmark Route Planner.")
            print("Goodbye!")
            break

        # Load the built-in landmark graph.
        if choice == 1:
            names, graph, default_start = sample_data()
            display_locations(names)
            start = select_location(
                names,
                f"Choose the starting location [{default_start + 1}]: "
            )
        else:
            # Let the user build a new custom graph.
            names, graph, start = custom_data()

        # Keep using the selected graph until returning to the main menu.
        while True:
            # Run Dijkstra's algorithm from the selected starting location.
            distances, previous = dijkstra(graph, start)

            print("\nRESULT DISPLAY OPTIONS")
            print("1. Show route to one destination")
            print("2. Show routes to every destination")

            display_choice = read_integer("Choose an option: ", 1, 2)

            # Display one selected shortest route.
            if display_choice == 1:
                display_locations(names)
                destination = select_location(
                    names,
                    "Choose the destination: "
                )

                display_single_route(
                    names,
                    distances,
                    previous,
                    start,
                    destination,
                )

            else:
                # Display shortest routes to all locations.
                display_all_results(
                    names,
                    distances,
                    previous,
                    start,
                )

            # ==========================
            # Navigation Menu
            # ==========================
            print("\n" + "=" * 41)
            print("1. Find another destination")
            print("2. Change starting location")
            print("3. Return to main menu")
            print("4. Exit")

            option = read_integer("\nChoose option: ", 1, 4)

            if option == 1:
                # Keep the same graph and starting location.
                continue

            elif option == 2:
                # Select a new starting location in the same graph.
                display_locations(names)
                start = select_location(
                    names,
                    "Choose the new starting location: "
                )
                continue

            elif option == 3:
                # Leave the graph and return to the main menu.
                break

            elif option == 4:
                # End the application immediately.
                print("\nThank you for using the Kuala Lumpur Landmark Route Planner.")
                print("Goodbye!")
                return


# Run main() only when this file is executed directly.
if __name__ == "__main__":
    main()