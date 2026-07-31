import unittest

from problem1_dijkstra.main import dijkstra, reconstruct_path, sample_data


class DijkstraTests(unittest.TestCase):
    def test_sample_shortest_distance_and_path(self):
        _, graph, start = sample_data()
        distances, previous = dijkstra(graph, start)
        self.assertEqual(distances[4], 10)
        self.assertEqual(reconstruct_path(previous, start, 4), [0, 2, 1, 3, 4])

    def test_unreachable_vertex(self):
        graph = [[0, 2, None], [2, 0, None], [None, None, 0]]
        distances, previous = dijkstra(graph, 0)
        self.assertEqual(distances[2], float("inf"))
        self.assertEqual(reconstruct_path(previous, 0, 2), [])

    def test_negative_edge_is_rejected(self):
        with self.assertRaises(ValueError):
            dijkstra([[0, -1], [-1, 0]], 0)


if __name__ == "__main__":
    unittest.main()
