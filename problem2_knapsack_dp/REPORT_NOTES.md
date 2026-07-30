# Problem 2 Report Notes: 0/1 Knapsack

Use these notes as source material for the Problem 2 and Testing and Validation
sections of the group report. Rewrite the explanations in the group's own words
after reviewing the implementation.

## Problem and Rationale

The 0/1 Knapsack problem receives a collection of items, each with an integer
weight and value, and a maximum capacity. The objective is to select a subset
whose total weight does not exceed the capacity and whose total value is as
large as possible. Each item can be selected once or excluded; fractions of an
item are not allowed.

Dynamic programming is suitable because many candidate solutions repeat the
same smaller item-and-capacity subproblems. The problem also has optimal
substructure: an optimal answer for the first `i` items depends on optimal
answers already computed for the first `i - 1` items.

## Algorithm

The program builds a table in which:

```text
table[i][w] = best value using the first i items with capacity w
```

For each item and capacity:

```text
exclude = table[i - 1][w]
include = item.value + table[i - 1][w - item.weight]
table[i][w] = the larger valid choice
```

The include choice is considered only when the current item fits. If include
and exclude have equal value, the program keeps the exclude result. This makes
ties deterministic by preferring the solution that does not add the later
item.

After filling the table, the program moves backwards through its rows. A value
that differs from the row above means that the corresponding item was selected.
Its weight is subtracted from the remaining capacity before backtracking
continues.

## Input and Output Design

The console program offers:

- A built-in sample for repeatable demonstrations.
- Custom item names, positive integer weights, non-negative integer values, and
  a non-negative integer capacity.
- Re-prompting when input is missing or outside the accepted range.
- An input table showing every available item.
- A results table showing the selected items, selected count, total weight,
  remaining capacity, and maximum value.

The DP table is returned from `solve_knapsack` for tests and explanation. It is
not printed during normal runs because it becomes too wide when capacity is
large.

## Built-in Sample

| Item | Weight | Value |
| --- | ---: | ---: |
| Item A | 3 | 10 |
| Item B | 4 | 12 |
| Item C | 2 | 7 |
| Item D | 5 | 14 |

Capacity: `7`

Expected result:

```text
Selected items: Item A and Item B
Selected count: 2
Total weight: 7
Remaining capacity: 0
Maximum value: 22
```

This optimum is unique: no other valid combination reaches value 22.

## Testing and Validation Evidence

| Test | Expected result | Actual result |
| --- | --- | --- |
| Built-in sample | A and B, weight 7, value 22 | Pass |
| Zero capacity | No items, value 0 | Pass |
| All items too heavy | No items, value 0 | Pass |
| Capacity holds every item | Every item selected and values summed | Pass |
| Smaller-item combination | Two smaller items beat one large item | Pass |
| Equal-value tie | Earlier item retained | Pass |
| Invalid capacity | `ValueError` | Pass |
| Invalid weight or value | `ValueError` | Pass |
| DP table check | Correct dimensions and final optimum | Pass |

Correctness was checked in three ways:

1. Manually calculate the expected result for small examples.
2. Confirm that the returned items never exceed capacity and their values sum
   to the returned maximum.
3. Run the automated tests in `test_knapsack.py`, including boundary cases and
   validation failures.

Run the tests with:

```bash
python3 -m unittest -v problem2_knapsack_dp.test_knapsack
```

## Complexity

For `n` items and integer capacity `W`:

- Time: `O(n x W)`.
- Memory: `O(n x W)`.

The two-dimensional table makes item reconstruction straightforward, but its
memory use grows with the numeric capacity.

## Strengths and Limitations

Strengths:

- Guarantees an optimal answer for valid integer inputs.
- Avoids recalculating overlapping subproblems.
- Returns both the optimum value and the selected items.
- Has deterministic tie behavior and repeatable tests.

Limitations:

- Table size grows with capacity rather than only with the number of items.
- Integer weights and capacity are required.
- It solves the 0/1 form only; an item cannot be split or selected repeatedly.

## Suggested Code Snippets

Include short extracts showing:

1. The include-versus-exclude recurrence.
2. The backtracking loop that recovers selected items.
3. Input validation for capacity, weights, and values.

Avoid pasting the complete program into the report body. The full source can be
placed in the appendix or submission folder.

## Screenshot Checklist

- [ ] Built-in input table.
- [ ] Built-in result showing A and B with value 22.
- [ ] One custom run with a different optimal combination.
- [ ] One invalid input followed by a valid replacement.
- [ ] Automated test summary.

## AI Usage Guidance

Suggested declaration to adapt:

> Generative AI assisted with hardening the initial implementation, identifying
> validation cases, expanding automated tests, and organizing documentation.
> The group reviewed the dynamic-programming recurrence and backtracking logic,
> manually checked sample calculations, ran the test suite, and verified that
> the selected items and reported totals were correct.
