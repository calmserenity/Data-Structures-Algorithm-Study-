import unittest

from problem3_tsp_genetic.main import (
    City,
    genetic_algorithm,
    ordered_crossover,
    route_distance,
)


class GeneticAlgorithmTests(unittest.TestCase):
    def test_route_closes_the_square(self):
        cities = [
            City("A", 0, 0),
            City("B", 0, 1),
            City("C", 1, 1),
            City("D", 1, 0),
        ]
        route, total = genetic_algorithm(cities, 30, 60, 0.1, seed=10)
        self.assertEqual(set(route), {0, 1, 2, 3})
        self.assertAlmostEqual(total, 4.0, places=6)

    def test_route_distance_includes_return_edge(self):
        cities = [City("A", 0, 0), City("B", 3, 0), City("C", 3, 4)]
        self.assertAlmostEqual(route_distance([0, 1, 2], cities), 12.0)

    def test_too_few_cities_is_rejected(self):
        with self.assertRaises(ValueError):
            genetic_algorithm([City("A", 0, 0), City("B", 1, 1)])


if __name__ == "__main__":
    unittest.main()

