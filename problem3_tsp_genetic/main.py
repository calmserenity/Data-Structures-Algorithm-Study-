"""Console program for TSP using a genetic algorithm.

Only Python's standard random-number and mathematics utilities are used.
The GA operations themselves are implemented explicitly below.
"""

import math
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class City:
    name: str
    x: float
    y: float


def distance(first, second):
    return math.sqrt((first.x - second.x) ** 2 + (first.y - second.y) ** 2)


def route_distance(route, cities):
    total = 0.0
    for index in range(len(route)):
        current = cities[route[index]]
        following = cities[route[(index + 1) % len(route)]]
        total += distance(current, following)
    return total


def random_route(city_count, rng):
    """Create a random permutation using manual Fisher-Yates shuffling."""
    route = list(range(city_count))
    for index in range(city_count - 1, 0, -1):
        swap_index = rng.randrange(index + 1)
        route[index], route[swap_index] = route[swap_index], route[index]
    return route


def tournament_selection(population, cities, rng, tournament_size=3):
    best = None
    best_distance = float("inf")
    for _ in range(tournament_size):
        candidate = population[rng.randrange(len(population))]
        candidate_distance = route_distance(candidate, cities)
        if candidate_distance < best_distance:
            best = candidate
            best_distance = candidate_distance
    return best[:]


def ordered_crossover(parent_one, parent_two, rng):
    """Create a valid permutation by preserving one parent segment."""
    size = len(parent_one)
    first = rng.randrange(size)
    second = rng.randrange(size)
    if first > second:
        first, second = second, first

    child = [None] * size
    child[first : second + 1] = parent_one[first : second + 1]

    insertion_index = (second + 1) % size
    scan_index = (second + 1) % size
    for _ in range(size):
        gene = parent_two[scan_index]
        if gene not in child:
            child[insertion_index] = gene
            insertion_index = (insertion_index + 1) % size
        scan_index = (scan_index + 1) % size

    return child


def mutate(route, mutation_rate, rng):
    child = route[:]
    if rng.random() < mutation_rate:
        first = rng.randrange(len(child))
        second = rng.randrange(len(child))
        child[first], child[second] = child[second], child[first]
    return child


def best_route(population, cities):
    best = population[0]
    best_distance = route_distance(best, cities)
    for candidate in population[1:]:
        candidate_distance = route_distance(candidate, cities)
        if candidate_distance < best_distance:
            best = candidate
            best_distance = candidate_distance
    return best[:], best_distance


def genetic_algorithm(
    cities,
    population_size=60,
    generations=150,
    mutation_rate=0.10,
    seed=2103,
):
    if len(cities) < 3:
        raise ValueError("At least three cities are required.")
    if population_size < 2 or generations < 1:
        raise ValueError("Population must be at least 2 and generations at least 1.")
    if not 0 <= mutation_rate <= 1:
        raise ValueError("Mutation rate must be between 0 and 1.")

    rng = random.Random(seed)
    population = [random_route(len(cities), rng) for _ in range(population_size)]
    overall_best, overall_distance = best_route(population, cities)

    for _ in range(generations):
        # Elitism keeps the best solution found in the next population.
        new_population = [overall_best[:]]

        while len(new_population) < population_size:
            parent_one = tournament_selection(population, cities, rng)
            parent_two = tournament_selection(population, cities, rng)
            child = ordered_crossover(parent_one, parent_two, rng)
            new_population.append(mutate(child, mutation_rate, rng))

        population = new_population
        generation_best, generation_distance = best_route(population, cities)
        if generation_distance < overall_distance:
            overall_best = generation_best
            overall_distance = generation_distance

    return overall_best, overall_distance


def sample_data():
    return [
        City("A", 0, 0),
        City("B", 0, 4),
        City("C", 3, 4),
        City("D", 3, 0),
        City("E", 1.5, 2),
    ]


def read_integer(prompt, minimum):
    while True:
        try:
            value = int(input(prompt))
            if value < minimum:
                raise ValueError
            return value
        except ValueError:
            print(f"Enter a whole number of at least {minimum}.")


def read_float(prompt, minimum=None, maximum=None):
    while True:
        try:
            value = float(input(prompt))
            if minimum is not None and value < minimum:
                raise ValueError
            if maximum is not None and value > maximum:
                raise ValueError
            return value
        except ValueError:
            print("Enter a valid number within the requested range.")


def custom_data():
    count = read_integer("Number of cities: ", 3)
    cities = []
    for index in range(count):
        print(f"City {index + 1}")
        name = input("  Name: ").strip() or f"City {index + 1}"
        x = read_float("  X coordinate: ")
        y = read_float("  Y coordinate: ")
        cities.append(City(name, x, y))
    return cities


def main():
    print("TSP USING A GENETIC ALGORITHM")
    choice = input("Use sample data? (Y/n): ").strip().lower()
    cities = sample_data() if choice != "n" else custom_data()

    best, total = genetic_algorithm(cities)
    names = [cities[index].name for index in best]
    names.append(names[0])

    print("\nGENETIC-ALGORITHM RESULTS")
    print("-" * 55)
    print("Best route found:", " -> ".join(names))
    print(f"Total distance: {total:.2f}")
    print("Population size: 60")
    print("Generations: 150")
    print("Mutation rate: 0.10")
    print("Random seed: 2103")


if __name__ == "__main__":
    main()

