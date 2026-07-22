import unittest

from problem2_knapsack_dp.main import Item, sample_data, solve_knapsack


class KnapsackTests(unittest.TestCase):
    def test_sample_optimum(self):
        items, capacity = sample_data()
        maximum_value, selected, _ = solve_knapsack(items, capacity)
        self.assertEqual(maximum_value, 22)
        self.assertEqual([item.name for item in selected], ["Item A", "Item B"])

    def test_zero_capacity(self):
        value, selected, _ = solve_knapsack([Item("A", 1, 5)], 0)
        self.assertEqual(value, 0)
        self.assertEqual(selected, [])

    def test_item_too_heavy(self):
        value, selected, _ = solve_knapsack([Item("A", 10, 50)], 5)
        self.assertEqual(value, 0)
        self.assertEqual(selected, [])


if __name__ == "__main__":
    unittest.main()

