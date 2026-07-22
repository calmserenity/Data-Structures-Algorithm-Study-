"""Console program for 0/1 Knapsack using dynamic programming."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    name: str
    weight: int
    value: int


def solve_knapsack(items, capacity):
    """Return maximum value, selected items, and the DP table."""
    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")
    for item in items:
        if item.weight <= 0 or item.value < 0:
            raise ValueError("Weights must be positive and values non-negative.")

    item_count = len(items)
    table = [[0 for _ in range(capacity + 1)] for _ in range(item_count + 1)]

    for item_number in range(1, item_count + 1):
        item = items[item_number - 1]
        for current_capacity in range(capacity + 1):
            exclude_value = table[item_number - 1][current_capacity]
            include_value = -1

            if item.weight <= current_capacity:
                include_value = (
                    item.value
                    + table[item_number - 1][current_capacity - item.weight]
                )

            table[item_number][current_capacity] = (
                include_value if include_value > exclude_value else exclude_value
            )

    selected = []
    remaining_capacity = capacity
    for item_number in range(item_count, 0, -1):
        if table[item_number][remaining_capacity] != table[item_number - 1][remaining_capacity]:
            item = items[item_number - 1]
            selected.append(item)
            remaining_capacity -= item.weight

    selected.reverse()
    return table[item_count][capacity], selected, table


def sample_data():
    items = [
        Item("Item A", 3, 10),
        Item("Item B", 4, 12),
        Item("Item C", 2, 7),
        Item("Item D", 5, 15),
    ]
    return items, 7


def read_integer(prompt, minimum):
    while True:
        try:
            value = int(input(prompt))
            if value < minimum:
                raise ValueError
            return value
        except ValueError:
            print(f"Enter a whole number of at least {minimum}.")


def custom_data():
    count = read_integer("Number of items: ", 1)
    items = []
    for index in range(count):
        print(f"Item {index + 1}")
        name = input("  Name: ").strip() or f"Item {index + 1}"
        weight = read_integer("  Weight: ", 1)
        value = read_integer("  Value: ", 0)
        items.append(Item(name, weight, value))
    capacity = read_integer("Maximum capacity: ", 0)
    return items, capacity


def display_results(maximum_value, selected, capacity):
    print("\nKNAPSACK RESULTS")
    print("-" * 50)
    if not selected:
        print("No items were selected.")
        return

    print(f"{'Item':<20}{'Weight':>10}{'Value':>10}")
    print("-" * 50)
    for item in selected:
        print(f"{item.name:<20}{item.weight:>10}{item.value:>10}")

    total_weight = sum(item.weight for item in selected)
    print("-" * 50)
    print(f"Total weight: {total_weight} / {capacity}")
    print(f"Maximum value: {maximum_value}")


def main():
    print("0/1 KNAPSACK USING DYNAMIC PROGRAMMING")
    choice = input("Use sample data? (Y/n): ").strip().lower()
    items, capacity = sample_data() if choice != "n" else custom_data()
    maximum_value, selected, _ = solve_knapsack(items, capacity)
    display_results(maximum_value, selected, capacity)


if __name__ == "__main__":
    main()

