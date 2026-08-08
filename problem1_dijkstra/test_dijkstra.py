"""Tests for the Dijkstra shortest-path implementation."""

import math
import unittest

from problem1_dijkstra.main import (
    INFINITY,
    dijkstra,
    kl_data,
    reconstruct_path,
)


class TestDijkstra(unittest.TestCase):
    def test_kl_sentral_to_klcc(self):
        names, graph, start = kl_data()
        distances, previous = dijkstra(graph, start)

        destination = names.index("KLCC")
        path = reconstruct_path(previous, start, destination)
        route = [names[index] for index in path]

        self.assertEqual(
            route,
            ["KL Sentral", "Pasar Seni", "Masjid Jamek", "KLCC"],
        )
        self.assertAlmostEqual(distances[destination], 6.3)

    def test_same_start_and_destination(self):
        graph = [
            [0, 4],
            [4, 0],
        ]

        distances, previous = dijkstra(graph, 1)

        self.assertEqual(reconstruct_path(previous, 1, 1), [1])
        self.assertEqual(distances[1], 0)

    def test_unreachable_destination(self):
        graph = [
            [0, 5, None],
            [5, 0, None],
            [None, None, 0],
        ]

        distances, previous = dijkstra(graph, 0)

        self.assertEqual(distances[2], INFINITY)
        self.assertEqual(reconstruct_path(previous, 0, 2), [])

    def test_shorter_indirect_route(self):
        graph = [
            [0, 4, 2, None],
            [4, 0, 1, 3],
            [2, 1, 0, 7],
            [None, 3, 7, 0],
        ]

        distances, previous = dijkstra(graph, 0)

        self.assertEqual(reconstruct_path(previous, 0, 3), [0, 2, 1, 3])
        self.assertEqual(distances[3], 6)

    def test_large_distance_is_supported(self):
        graph = [
            [0, 10_000_001],
            [10_000_001, 0],
        ]

        distances, previous = dijkstra(graph, 0)

        self.assertEqual(distances[1], 10_000_001)
        self.assertEqual(reconstruct_path(previous, 0, 1), [0, 1])

    def test_empty_graph_is_rejected(self):
        with self.assertRaises(ValueError):
            dijkstra([], 0)

    def test_non_square_graph_is_rejected(self):
        graph = [
            [0, 1],
            [1],
        ]

        with self.assertRaises(ValueError):
            dijkstra(graph, 0)

    def test_negative_start_is_rejected(self):
        graph = [
            [0, 2],
            [2, 0],
        ]

        with self.assertRaises(ValueError):
            dijkstra(graph, -1)

    def test_start_outside_graph_is_rejected(self):
        graph = [
            [0, 2],
            [2, 0],
        ]

        with self.assertRaises(ValueError):
            dijkstra(graph, 2)

    def test_negative_edge_is_rejected(self):
        graph = [
            [0, -2],
            [-2, 0],
        ]

        with self.assertRaises(ValueError):
            dijkstra(graph, 0)

    def test_negative_edge_in_disconnected_section_is_rejected(self):
        graph = [
            [0, 1, None, None],
            [1, 0, None, None],
            [None, None, 0, -5],
            [None, None, -5, 0],
        ]

        with self.assertRaises(ValueError):
            dijkstra(graph, 0)

    def test_nan_edge_is_rejected(self):
        graph = [
            [0, math.nan],
            [math.nan, 0],
        ]

        with self.assertRaises(ValueError):
            dijkstra(graph, 0)

    def test_positive_infinity_edge_is_rejected(self):
        graph = [
            [0, math.inf],
            [math.inf, 0],
        ]

        with self.assertRaises(ValueError):
            dijkstra(graph, 0)

    def test_negative_infinity_edge_is_rejected(self):
        graph = [
            [0, -math.inf],
            [-math.inf, 0],
        ]

        with self.assertRaises(ValueError):
            dijkstra(graph, 0)

    def test_non_numeric_edge_is_rejected(self):
        graph = [
            [0, "three"],
            ["three", 0],
        ]

        with self.assertRaises(ValueError):
            dijkstra(graph, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
