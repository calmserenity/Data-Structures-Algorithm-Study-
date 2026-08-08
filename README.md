# Data Structures and Algorithms Study

This repository contains three independent console-based Python programs for
the CSC2103 group assignment:

1. `problem1_dijkstra` - Dijkstra's greedy shortest-path algorithm.
2. `problem2_knapsack_dp` - 0/1 Knapsack using dynamic programming.
3. `problem3_tsp_genetic` - Travelling Salesman Problem using a genetic
   algorithm.

Each problem folder contains the program, automated tests, and notes that can
be adapted for the assignment report.

## Requirements

- Python 3.10 or newer.
- No external packages.

The core algorithms use only code written in this repository. Standard-library
utilities are used for data classes, console input, mathematics, random-number
generation, and automated testing.

## Run Problem 1: Dijkstra's Shortest Path

From the repository root:

```bash
python3 problem1_dijkstra/main.py
```

Choose the built-in Kuala Lumpur landmark network or create a custom undirected
network of 2 to 20 locations. The results menu can display one shortest route,
all shortest routes from the selected start, or a greedy selection trace showing
which location was finalized at each stage and which neighbour distances
improved. The built-in distances are illustrative demonstration data.

The reproducible sample route from KL Sentral to KLCC is:

```text
KL Sentral -> Pasar Seni -> Masjid Jamek -> KLCC
Total distance: 6.30 km
```

## Run Problem 2: 0/1 Knapsack

From the repository root:

```bash
python3 problem2_knapsack_dp/main.py
```

Press Enter at the first prompt to use the built-in sample. Enter `n` to provide
your own item names, integer weights, integer values, and knapsack capacity.
Invalid values are rejected and requested again.

The sample has capacity 7 and the following unique optimum:

```text
Selected items: Item A, Item B
Total weight: 7 / 7
Maximum value: 22
```

The completed dynamic-programming table is returned by `solve_knapsack` for
testing and explanation, but it is not printed because large capacities can
make it too wide for a console.

## Run Problem 3: TSP Genetic Algorithm

From the repository root:

```bash
python3 problem3_tsp_genetic/main.py
```

Press Enter to use the built-in cities or enter `n` to provide at least three
city names and coordinates. After the cities are displayed, choose either the
default genetic settings or custom settings.

The defaults are:

| Setting | Value |
| --- | ---: |
| Population size | 60 |
| Generations | 150 |
| Mutation rate | 0.10 |
| Random seed | 2103 |

The fixed seed makes the default sample reproducible for testing and report
screenshots. A genetic algorithm is heuristic: it aims to find a short route
efficiently but does not guarantee the global optimum for every input.

## Run Tests

Run an individual problem suite:

```bash
python3 -m unittest -v problem1_dijkstra.test_dijkstra
python3 -m unittest -v problem2_knapsack_dp.test_knapsack problem3_tsp_genetic.test_genetic
```

Run all three problem suites:

```bash
python3 -m unittest -v problem1_dijkstra.test_dijkstra problem2_knapsack_dp.test_knapsack problem3_tsp_genetic.test_genetic
```

## Before Submission

- Run both sample and custom-input paths.
- Add or adapt test cases that the group can explain.
- Capture readable screenshots of inputs and results.
- Transfer the relevant material from each `REPORT_NOTES.md` into the final
  report.
- Include expected-versus-actual results and explain how correctness was
  checked.
- Ensure every member understands Dijkstra's greedy choice and relaxation, the
  recurrence used by 0/1 Knapsack, and the genetic operators used by TSP.
- Declare the parts assisted by generative AI and explain how the group manually
  reviewed and verified them.
