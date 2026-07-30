"""Five test cases for the Dijkstra route planner."""

import unittest

from dijkstra import INFINITY, dijkstra, reconstruct_path, kl_data


class TestDijkstra(unittest.TestCase):

    def test_kl_sentral_to_klcc(self):
        """Test the shortest route using the built-in KL data."""
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
        """Test when the starting location is also the destination."""
        graph = [
            [0, 4],
            [4, 0],
        ]

        distances, previous = dijkstra(graph, 1)
        path = reconstruct_path(previous, 1, 1)

        self.assertEqual(path, [1])
        self.assertEqual(distances[1], 0)

    def test_unreachable_destination(self):
        """Test a destination that is disconnected from the graph."""
        graph = [
            [0, 5, None],
            [5, 0, None],
            [None, None, 0],
        ]

        distances, previous = dijkstra(graph, 0)
        path = reconstruct_path(previous, 0, 2)

        self.assertEqual(distances[2], INFINITY)
        self.assertEqual(path, [])

    def test_shorter_indirect_route(self):
        """Test that a shorter indirect route is selected."""
        graph = [
            [0, 4, 2, None],
            [4, 0, 1, 3],
            [2, 1, 0, 7],
            [None, 3, 7, 0],
        ]

        distances, previous = dijkstra(graph, 0)
        path = reconstruct_path(previous, 0, 3)

        # Shortest route: 0 -> 2 -> 1 -> 3
        self.assertEqual(path, [0, 2, 1, 3])
        self.assertEqual(distances[3], 6)

    def test_negative_edge_error(self):
        """Test that negative edge weights are rejected."""
        graph = [
            [0, -2],
            [-2, 0],
        ]

        with self.assertRaises(ValueError):
            dijkstra(graph, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)