import io
import random
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from problem3_tsp_genetic import main as tsp_program
from problem3_tsp_genetic.main import (
    City,
    genetic_algorithm,
    mutate,
    ordered_crossover,
    read_float,
    route_distance,
    sample_data,
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

    def test_triangle_has_known_total_distance(self):
        cities = [City("A", 0, 0), City("B", 3, 0), City("C", 0, 4)]
        route, total = genetic_algorithm(cities, 12, 20, 0.1, seed=5)
        self.assertEqual(set(route), {0, 1, 2})
        self.assertAlmostEqual(total, 12.0)

    def test_ordered_crossover_produces_valid_permutation(self):
        parent_one = [0, 1, 2, 3, 4, 5]
        parent_two = [5, 4, 3, 2, 1, 0]
        child = ordered_crossover(parent_one, parent_two, random.Random(12))
        self.assertEqual(len(child), len(parent_one))
        self.assertEqual(set(child), set(parent_one))

    def test_mutation_preserves_valid_permutation(self):
        route = [0, 1, 2, 3, 4]
        child = mutate(route, 1.0, random.Random(8))
        self.assertEqual(len(child), len(route))
        self.assertEqual(set(child), set(route))
        self.assertEqual(route, [0, 1, 2, 3, 4])

    def test_same_seed_is_reproducible(self):
        cities = sample_data()
        first_route, first_distance = genetic_algorithm(cities, seed=27)
        second_route, second_distance = genetic_algorithm(cities, seed=27)
        self.assertEqual(first_route, second_route)
        self.assertEqual(first_distance, second_distance)

    def test_returned_route_starts_with_first_city(self):
        route, _ = genetic_algorithm(sample_data(), seed=37)
        self.assertEqual(route[0], 0)

    def test_too_few_cities_is_rejected(self):
        with self.assertRaises(ValueError):
            genetic_algorithm([City("A", 0, 0), City("B", 1, 1)])

    def test_invalid_genetic_settings_are_rejected(self):
        cities = sample_data()
        invalid_settings = [
            {"population_size": 1},
            {"population_size": 2.5},
            {"generations": 0},
            {"generations": 1.5},
            {"mutation_rate": -0.01},
            {"mutation_rate": 1.01},
            {"mutation_rate": float("nan")},
            {"seed": 2.5},
        ]
        for settings in invalid_settings:
            with self.subTest(settings=settings):
                with self.assertRaises(ValueError):
                    genetic_algorithm(cities, **settings)

    def test_non_finite_coordinates_are_rejected(self):
        for coordinate in (float("nan"), float("inf"), float("-inf")):
            cities = [
                City("A", coordinate, 0),
                City("B", 1, 0),
                City("C", 0, 1),
            ]
            with self.subTest(coordinate=coordinate):
                with self.assertRaises(ValueError):
                    genetic_algorithm(cities)

    def test_float_reader_reprompts_after_non_finite_input(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["nan", "infinity", "0.25"]):
            with redirect_stdout(output):
                value = read_float("Rate: ", 0, 1)
        self.assertEqual(value, 0.25)
        self.assertEqual(output.getvalue().count("valid number"), 2)

    def test_sample_console_run_shows_route_settings_and_notice(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["", ""]):
            with redirect_stdout(output):
                tsp_program.main()

        text = output.getvalue()
        self.assertIn("INPUT CITIES", text)
        self.assertIn("Best route found:", text)
        self.assertIn("Total distance: 15.00", text)
        self.assertIn("Population size: 60", text)
        self.assertIn("Generations: 150", text)
        self.assertIn("Mutation rate: 0.10", text)
        self.assertIn("Random seed: 2103", text)
        self.assertIn("not guaranteed to be globally optimal", text)

    def test_custom_genetic_settings_are_used_and_displayed(self):
        output = io.StringIO()
        answers = ["", "n", "12", "20", "0.001", "99"]
        with patch("builtins.input", side_effect=answers):
            with redirect_stdout(output):
                tsp_program.main()

        text = output.getvalue()
        self.assertIn("Population size: 12", text)
        self.assertIn("Generations: 20", text)
        self.assertIn("Mutation rate: 0.001", text)
        self.assertIn("Random seed: 99", text)


if __name__ == "__main__":
    unittest.main()
