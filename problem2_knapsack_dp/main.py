"""Console program for 0/1 Knapsack using dynamic programming."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    name: str
    weight: int
    value: int


def solve_knapsack(items, capacity):
    """Return the maximum value, selected items, and completed DP table.

    ``table[i][w]`` stores the best value obtainable from the first ``i``
    items when the knapsack capacity is ``w``.
    """
    if type(capacity) is not int or capacity < 0:
        raise ValueError("Capacity must be a non-negative integer.")

    for item in items:
        if not isinstance(item, Item):
            raise ValueError("Every item must be an Item instance.")
        if type(item.weight) is not int or item.weight <= 0:
            raise ValueError("Every item weight must be a positive integer.")
        if type(item.value) is not int or item.value < 0:
            raise ValueError("Every item value must be a non-negative integer.")

    item_count = len(items)
    table = [[0 for _ in range(capacity + 1)] for _ in range(item_count + 1)]

    # Reusing the previous row solves the overlapping subproblems only once.
    # The recurrence also shows optimal substructure: the best answer is the
    # better of excluding the current item or including it when it fits.
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

            # Strictly greater preserves a deterministic tie rule: if both
            # choices have equal value, the later item remains excluded.
            table[item_number][current_capacity] = (
                include_value if include_value > exclude_value else exclude_value
            )

    # Walk backwards through the completed table. A changed value means that
    # the current item was used by the optimal solution for this capacity.
    selected = []
    remaining_capacity = capacity
    for item_number in range(item_count, 0, -1):
        if (
            table[item_number][remaining_capacity]
            != table[item_number - 1][remaining_capacity]
        ):
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
        Item("Item D", 5, 14),
    ]
    return items, 7


def read_yes_no(prompt, default=True):
    """Read a yes/no answer, using ``default`` when Enter is pressed."""
    while True:
        answer = input(prompt).strip().lower()
        if not answer:
            return default
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Enter Y for yes or N for no.")


def read_integer(prompt, minimum, maximum=None):
    """Read an integer within the inclusive requested range."""
    while True:
        try:
            value = int(input(prompt))
            if value < minimum or (maximum is not None and value > maximum):
                raise ValueError
            return value
        except ValueError:
            if maximum is None:
                print(f"Enter a whole number of at least {minimum}.")
            else:
                print(f"Enter a whole number from {minimum} to {maximum}.")


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


def display_items(items, capacity):
    """Display all available items before solving the problem."""
    print("\nAVAILABLE ITEMS")
    print("-" * 56)
    print(f"{'No.':<6}{'Item':<24}{'Weight':>12}{'Value':>12}")
    print("-" * 56)
    for number, item in enumerate(items, start=1):
        print(f"{number:<6}{item.name:<24}{item.weight:>12}{item.value:>12}")
    print("-" * 56)
    print(f"Knapsack capacity: {capacity}")


def display_results(maximum_value, selected, capacity):
    print("\nKNAPSACK RESULTS")
    print("-" * 56)
    if not selected:
        print("No items were selected.")
    else:
        print(f"{'Item':<28}{'Weight':>14}{'Value':>14}")
        print("-" * 56)
        for item in selected:
            print(f"{item.name:<28}{item.weight:>14}{item.value:>14}")

    total_weight = sum(item.weight for item in selected)
    print("-" * 56)
    print(f"Selected items: {len(selected)}")
    print(f"Total weight: {total_weight} / {capacity}")
    print(f"Remaining capacity: {capacity - total_weight}")
    print(f"Maximum value: {maximum_value}")


def main():
    print("0/1 KNAPSACK USING DYNAMIC PROGRAMMING")
    use_sample = read_yes_no("Use sample data? (Y/n): ", default=True)
    items, capacity = sample_data() if use_sample else custom_data()
    display_items(items, capacity)
    maximum_value, selected, _ = solve_knapsack(items, capacity)
    display_results(maximum_value, selected, capacity)


if __name__ == "__main__":
    main()
