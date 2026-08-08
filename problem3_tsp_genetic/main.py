"""Package-delivery route optimizer using a genetic algorithm.

Only Python's standard random-number and mathematics utilities are used.
The GA operations and route evaluation are implemented explicitly below.
"""

import math
import random
from dataclasses import dataclass


DEFAULT_POPULATION_SIZE = 60
DEFAULT_GENERATIONS = 150
DEFAULT_MUTATION_RATE = 0.10
DEFAULT_SEED = 2103


@dataclass(frozen=True)
class DeliveryPoint:
    """A depot or package-delivery stop on a two-dimensional map."""

    name: str
    x: float
    y: float


@dataclass
class EvaluatedRoute:
    """Keep a candidate route together with its cached distance."""

    route: list
    distance: float


def distance(first, second):
    return math.sqrt((first.x - second.x) ** 2 + (first.y - second.y) ** 2)


def route_distance(route, delivery_points):
    total = 0.0
    for index in range(len(route)):
        current = delivery_points[route[index]]
        following = delivery_points[route[(index + 1) % len(route)]]
        total += distance(current, following)
    return total


def build_distance_matrix(delivery_points):
    """Precompute every symmetric point-to-point distance once."""
    point_count = len(delivery_points)
    matrix = [
        [0.0 for _ in range(point_count)]
        for _ in range(point_count)
    ]

    for first in range(point_count):
        for second in range(first + 1, point_count):
            value = distance(delivery_points[first], delivery_points[second])
            matrix[first][second] = value
            matrix[second][first] = value

    return matrix


def route_distance_from_matrix(route, distance_matrix):
    """Return a closed-tour distance using precomputed edge distances."""
    total = 0.0
    for index in range(len(route)):
        current = route[index]
        following = route[(index + 1) % len(route)]
        total += distance_matrix[current][following]
    return total


def random_route(point_count, rng):
    """Create a random permutation using manual Fisher-Yates shuffling."""
    route = list(range(point_count))
    for index in range(point_count - 1, 0, -1):
        swap_index = rng.randrange(index + 1)
        route[index], route[swap_index] = route[swap_index], route[index]
    return route


def tournament_selection(population, rng, tournament_size=3):
    """Select a route by comparing evaluated candidates."""
    best = population[rng.randrange(len(population))]
    for _ in range(tournament_size - 1):
        candidate = population[rng.randrange(len(population))]
        if candidate.distance < best.distance:
            best = candidate
    return best.route[:]


def ordered_crossover(parent_one, parent_two, rng):
    """Create a valid permutation by preserving one parent segment."""
    size = len(parent_one)
    first = rng.randrange(size)
    second = rng.randrange(size)
    if first > second:
        first, second = second, first

    child = [None] * size
    used = [False] * size
    for index in range(first, second + 1):
        gene = parent_one[index]
        child[index] = gene
        used[gene] = True

    insertion_index = (second + 1) % size
    scan_index = (second + 1) % size
    for _ in range(size):
        gene = parent_two[scan_index]
        if not used[gene]:
            child[insertion_index] = gene
            used[gene] = True
            insertion_index = (insertion_index + 1) % size
        scan_index = (scan_index + 1) % size

    return child


def mutate(route, mutation_rate, rng):
    """Return a copy, occasionally swapping two city positions."""
    child = route[:]
    if len(child) >= 2 and rng.random() < mutation_rate:
        first = rng.randrange(len(child))
        second = rng.randrange(len(child) - 1)
        if second >= first:
            second += 1
        child[first], child[second] = child[second], child[first]
    return child


def best_route(population):
    """Return the route with the smallest cached distance."""
    best = population[0]
    for candidate in population[1:]:
        if candidate.distance < best.distance:
            best = candidate
    return best.route[:], best.distance


def normalize_route(route, depot_index=0):
    """Rotate a cyclic route so that the depot is shown first."""
    for position, point_index in enumerate(route):
        if point_index == depot_index:
            return route[position:] + route[:position]
    raise ValueError("The requested depot is not present in the route.")


def genetic_algorithm(
    delivery_points,
    population_size=DEFAULT_POPULATION_SIZE,
    generations=DEFAULT_GENERATIONS,
    mutation_rate=DEFAULT_MUTATION_RATE,
    seed=DEFAULT_SEED,
):
    """Find a short depot-to-deliveries round trip using a genetic algorithm."""
    if len(delivery_points) < 3:
        raise ValueError("A depot and at least two delivery stops are required.")
    for point in delivery_points:
        if not isinstance(point, DeliveryPoint):
            raise ValueError("Every location must be a DeliveryPoint instance.")
        try:
            coordinates_are_finite = math.isfinite(point.x) and math.isfinite(point.y)
        except TypeError as error:
            raise ValueError("Location coordinates must be finite numbers.") from error
        if not coordinates_are_finite:
            raise ValueError("Location coordinates must be finite numbers.")

    if type(population_size) is not int or population_size < 2:
        raise ValueError("Population size must be an integer of at least 2.")
    if type(generations) is not int or generations < 1:
        raise ValueError("Generations must be an integer of at least 1.")
    if (
        isinstance(mutation_rate, bool)
        or not isinstance(mutation_rate, (int, float))
        or not math.isfinite(mutation_rate)
        or not 0 <= mutation_rate <= 1
    ):
        raise ValueError("Mutation rate must be between 0 and 1.")
    if type(seed) is not int:
        raise ValueError("Random seed must be an integer.")

    rng = random.Random(seed)
    distance_matrix = build_distance_matrix(delivery_points)
    population = []
    for _ in range(population_size):
        route = random_route(len(delivery_points), rng)
        population.append(
            EvaluatedRoute(
                route=route,
                distance=route_distance_from_matrix(route, distance_matrix),
            )
        )
    overall_best, overall_distance = best_route(population)

    for _ in range(generations):
        # Elitism keeps the best solution found in the next population.
        new_population = [EvaluatedRoute(overall_best[:], overall_distance)]

        while len(new_population) < population_size:
            parent_one = tournament_selection(population, rng)
            parent_two = tournament_selection(population, rng)
            child = ordered_crossover(parent_one, parent_two, rng)
            child = mutate(child, mutation_rate, rng)
            child_distance = route_distance_from_matrix(child, distance_matrix)
            new_population.append(EvaluatedRoute(child, child_distance))

        population = new_population
        generation_best, generation_distance = best_route(population)
        if generation_distance < overall_distance:
            overall_best = generation_best
            overall_distance = generation_distance

    # A tour is cyclic, so rotating it to the first input city changes only
    # presentation and not its total distance.
    return normalize_route(overall_best), overall_distance


def sample_data():
    return [
        DeliveryPoint("Distribution Depot", 0, 0),
        DeliveryPoint("Package A - Office Tower", 0, 4),
        DeliveryPoint("Package B - Apartment", 3, 4),
        DeliveryPoint("Package C - Retail Store", 3, 0),
        DeliveryPoint("Package D - Service Centre", 1.5, 2),
    ]


def read_yes_no(prompt, default=True):
    """Read a yes/no answer, using ``default`` when Enter is pressed."""
    while True:
        answer = input(prompt).strip().lower()
        if not answer:
            return default
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Enter Y for yes or N for no.")


def read_integer(prompt, minimum=None, maximum=None):
    """Read an integer within optional inclusive bounds."""
    while True:
        try:
            value = int(input(prompt))
            if minimum is not None and value < minimum:
                raise ValueError
            if maximum is not None and value > maximum:
                raise ValueError
            return value
        except ValueError:
            if minimum is None and maximum is None:
                print("Enter a whole number.")
            elif maximum is None:
                print(f"Enter a whole number of at least {minimum}.")
            elif minimum is None:
                print(f"Enter a whole number no greater than {maximum}.")
            else:
                print(f"Enter a whole number from {minimum} to {maximum}.")


def read_float(prompt, minimum=None, maximum=None):
    while True:
        try:
            value = float(input(prompt))
            if not math.isfinite(value):
                raise ValueError
            if minimum is not None and value < minimum:
                raise ValueError
            if maximum is not None and value > maximum:
                raise ValueError
            return value
        except ValueError:
            print("Enter a valid number within the requested range.")


def custom_data():
    print("\nDEPOT")
    depot_name = input("  Name: ").strip() or "Distribution Depot"
    depot_x = read_float("  X coordinate: ")
    depot_y = read_float("  Y coordinate: ")
    delivery_points = [DeliveryPoint(depot_name, depot_x, depot_y)]

    stop_count = read_integer("Number of delivery stops (at least 2): ", 2)
    for index in range(stop_count):
        print(f"Delivery stop {index + 1}")
        name = input("  Package/destination: ").strip()
        if not name:
            name = f"Package {index + 1}"
        x = read_float("  X coordinate: ")
        y = read_float("  Y coordinate: ")
        delivery_points.append(DeliveryPoint(name, x, y))
    return delivery_points


def read_genetic_settings():
    """Return default settings or validated settings entered by the user."""
    use_defaults = read_yes_no(
        "Use default genetic settings? (Y/n): ",
        default=True,
    )
    if use_defaults:
        return (
            DEFAULT_POPULATION_SIZE,
            DEFAULT_GENERATIONS,
            DEFAULT_MUTATION_RATE,
            DEFAULT_SEED,
        )

    population_size = read_integer("Population size (at least 2): ", 2)
    generations = read_integer("Number of generations (at least 1): ", 1)
    mutation_rate = read_float("Mutation rate (0 to 1): ", 0, 1)
    seed = read_integer("Random seed (whole number): ")
    return population_size, generations, mutation_rate, seed


def display_delivery_points(delivery_points):
    """Display the depot, delivery stops, and their coordinates."""
    print("\nDELIVERY POINTS")
    print("-" * 58)
    print(f"{'Type':<10}{'Location':<22}{'X':>13}{'Y':>13}")
    print("-" * 58)
    for index, point in enumerate(delivery_points):
        point_type = "Depot" if index == 0 else f"Stop {index}"
        print(f"{point_type:<10}{point.name:<22}{point.x:>13g}{point.y:>13g}")
    print("-" * 58)


def display_results(
    route,
    total_distance,
    delivery_points,
    population_size,
    generations,
    mutation_rate,
    seed,
):
    """Display the delivery route, distance, settings, and heuristic caveat."""
    names = [delivery_points[index].name for index in route]
    names.append(names[0])
    mutation_rate_text = format(mutation_rate, ".15g")
    if "e" not in mutation_rate_text.lower():
        if "." not in mutation_rate_text:
            mutation_rate_text += ".00"
        else:
            decimal_places = len(mutation_rate_text.split(".", 1)[1])
            mutation_rate_text += "0" * max(0, 2 - decimal_places)

    print("\nPACKAGE-DELIVERY ROUTE")
    print("-" * 58)
    print("Optimized route:", " -> ".join(names))
    print(f"Total distance: {total_distance:.2f}")
    print(f"Packages delivered: {len(delivery_points) - 1}")
    print(f"Population size: {population_size}")
    print(f"Generations: {generations}")
    print(f"Mutation rate: {mutation_rate_text}")
    print(f"Random seed: {seed}")
    print(
        "Note: This is a heuristic result and is not guaranteed "
        "to be globally optimal."
    )


def main():
    print("PACKAGE DELIVERY OPTIMIZER USING A GENETIC ALGORITHM")
    use_sample = read_yes_no("Use sample delivery data? (Y/n): ", default=True)
    delivery_points = sample_data() if use_sample else custom_data()
    display_delivery_points(delivery_points)

    population_size, generations, mutation_rate, seed = read_genetic_settings()
    best, total = genetic_algorithm(
        delivery_points,
        population_size,
        generations,
        mutation_rate,
        seed,
    )
    display_results(
        best,
        total,
        delivery_points,
        population_size,
        generations,
        mutation_rate,
        seed,
    )


if __name__ == "__main__":
    main()
