"""Tests for the Dijkstra shortest-path implementation."""

import io
import math
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from problem1_dijkstra.main import (
    INFINITY,
    dijkstra,
    display_greedy_trace,
    kl_data,
    main,
    reconstruct_path,
    select_location,
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

    def test_zero_weight_edge_is_supported(self):
        graph = [
            [0, 0, 5],
            [0, 0, 2],
            [5, 2, 0],
        ]

        distances, previous = dijkstra(graph, 0)

        self.assertEqual(distances, [0, 0, 2])
        self.assertEqual(reconstruct_path(previous, 0, 2), [0, 1, 2])

    def test_trace_records_greedy_order_and_relaxations(self):
        graph = [
            [0, 4, 2, None],
            [4, 0, 1, 3],
            [2, 1, 0, 7],
            [None, 3, 7, 0],
        ]

        distances, previous, trace = dijkstra(
            graph,
            0,
            include_trace=True,
        )

        self.assertEqual([step.selected for step in trace], [0, 2, 1, 3])
        self.assertEqual(trace[0].updates, ((1, INFINITY, 4), (2, INFINITY, 2)))
        self.assertEqual(trace[1].updates, ((1, 4, 3), (3, INFINITY, 9)))
        self.assertEqual(distances[3], 6)
        self.assertEqual(reconstruct_path(previous, 0, 3), [0, 2, 1, 3])

    def test_trace_display_explains_the_greedy_choice(self):
        names = ["A", "B", "C"]
        graph = [
            [0, 2, 5],
            [2, 0, 1],
            [5, 1, 0],
        ]
        _, _, trace = dijkstra(graph, 0, include_trace=True)
        output = io.StringIO()

        with redirect_stdout(output):
            display_greedy_trace(names, trace)

        displayed = output.getvalue()
        self.assertIn("GREEDY SELECTION TRACE", displayed)
        self.assertIn("A", displayed)
        self.assertIn("Improved neighbours:", displayed)
        self.assertIn("B: Unreachable -> 2.00 km", displayed)
        self.assertIn("C: Unreachable -> 5.00 km", displayed)
        self.assertIn("choose the nearest unvisited location", displayed)

    def test_location_reader_accepts_displayed_default(self):
        with patch("builtins.input", return_value=""):
            self.assertEqual(select_location(["A", "B"], "Location [1]: ", 0), 0)

    def test_sample_console_run_can_show_greedy_trace(self):
        output = io.StringIO()
        inputs = ["1", "", "3", "4"]

        with patch("builtins.input", side_effect=inputs), redirect_stdout(output):
            main()

        displayed = output.getvalue()
        self.assertIn("KUALA LUMPUR LANDMARK ROUTE PLANNER", displayed)
        self.assertIn("GREEDY SELECTION TRACE", displayed)
        self.assertIn("KL Sentral", displayed)
        self.assertIn("Greedy rule:", displayed)

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
