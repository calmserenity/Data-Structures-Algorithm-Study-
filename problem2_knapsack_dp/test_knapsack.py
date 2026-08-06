import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from problem2_knapsack_dp import main as knapsack_program
from problem2_knapsack_dp.main import Item, read_integer, sample_data, solve_knapsack


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

    def test_capacity_can_hold_every_item(self):
        items = [Item("A", 2, 4), Item("B", 3, 7), Item("C", 1, 2)]
        value, selected, _ = solve_knapsack(items, 6)
        self.assertEqual(value, 13)
        self.assertEqual(selected, items)

    def test_smaller_items_can_beat_one_large_item(self):
        items = [
            Item("Large", 5, 9),
            Item("Small A", 2, 5),
            Item("Small B", 3, 6),
        ]
        value, selected, _ = solve_knapsack(items, 5)
        self.assertEqual(value, 11)
        self.assertEqual([item.name for item in selected], ["Small A", "Small B"])

    def test_equal_value_tie_keeps_earlier_item(self):
        items = [Item("Earlier", 2, 5), Item("Later", 2, 5)]
        value, selected, _ = solve_knapsack(items, 2)
        self.assertEqual(value, 5)
        self.assertEqual([item.name for item in selected], ["Earlier"])

    def test_dp_table_dimensions_and_final_value(self):
        items = [Item("A", 1, 2), Item("B", 2, 3)]
        value, _, table = solve_knapsack(items, 3)
        self.assertEqual(len(table), len(items) + 1)
        self.assertTrue(all(len(row) == 4 for row in table))
        self.assertEqual(table[-1][-1], value)
        self.assertEqual(value, 5)

    def test_invalid_capacity_is_rejected(self):
        for capacity in (-1, 2.5, True):
            with self.subTest(capacity=capacity):
                with self.assertRaises(ValueError):
                    solve_knapsack([Item("A", 1, 1)], capacity)

    def test_non_positive_or_non_integer_weight_is_rejected(self):
        for weight in (0, -1, 1.5, True):
            with self.subTest(weight=weight):
                with self.assertRaises(ValueError):
                    solve_knapsack([Item("A", weight, 1)], 5)

    def test_negative_or_non_integer_value_is_rejected(self):
        for item_value in (-1, 1.5, True):
            with self.subTest(value=item_value):
                with self.assertRaises(ValueError):
                    solve_knapsack([Item("A", 1, item_value)], 5)

    def test_integer_reader_reprompts_after_invalid_input(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["not a number", "0", "3"]):
            with redirect_stdout(output):
                value = read_integer("Value: ", 1)
        self.assertEqual(value, 3)
        self.assertEqual(output.getvalue().count("at least 1"), 2)

    def test_sample_console_run_shows_inputs_and_totals(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=[""]):
            with redirect_stdout(output):
                knapsack_program.main()

        text = output.getvalue()
        self.assertIn("AVAILABLE ITEMS", text)
        self.assertIn("Knapsack capacity: 7", text)
        self.assertIn("Item A", text)
        self.assertIn("Item B", text)
        self.assertIn("Selected items: 2", text)
        self.assertIn("Total weight: 7 / 7", text)
        self.assertIn("Remaining capacity: 0", text)
        self.assertIn("Maximum value: 22", text)


if __name__ == "__main__":
    unittest.main()
