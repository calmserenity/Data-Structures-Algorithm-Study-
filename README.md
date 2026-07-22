# Data Structures & Algorithm 

This project contains three independent console-based Python programs:

1. `problem1_dijkstra` - Dijkstra's greedy shortest-path algorithm
2. `problem2_knapsack_dp` - 0/1 Knapsack using dynamic programming
3. `problem3_tsp_genetic` - Travelling Salesman Problem using a genetic algorithm

Each problem folder contains its own program, tests, and notes for the report.

## Requirements

- Python 3.10 or newer
- No external packages are required

## Run a program

From this project folder:

```powershell
python problem1_dijkstra/main.py
python problem2_knapsack_dp/main.py
python problem3_tsp_genetic/main.py
```

Each program offers built-in sample data as well as custom keyboard input.

## Run all tests

```powershell
python -m unittest -v problem1_dijkstra.test_dijkstra problem2_knapsack_dp.test_knapsack problem3_tsp_genetic.test_genetic
```

## Before submission

- Replace or extend the sample data with your group's own test cases.
- Make sure every member understands and can explain the algorithms.
- Capture screenshots of meaningful program runs.
- Complete each folder's `REPORT_NOTES.md`.
- Include expected-versus-actual results in the report.
- Declare that AI assisted with the initial project structure and code boilerplate.
- Verify the source code manually and modify it as your group considers appropriate.

