# Problem 3 Report Notes: TSP Genetic Algorithm

Use these notes as source material for the Problem 3 and Testing and Validation
sections of the group report. Rewrite the explanations in the group's own words
after reviewing every genetic operator.

## Problem and Rationale

The Travelling Salesman Problem asks for a shortest closed route that visits
every city exactly once and returns to its starting city. The number of possible
routes grows very quickly as cities are added, so exhaustive search becomes
impractical.

A genetic algorithm is a heuristic approach. It searches many candidate routes
and evolves them toward shorter distances. It can efficiently find a good route
but does not guarantee the global optimum for every data set.

## Route Representation and Distance

A chromosome is a permutation of city indexes. For example:

```text
[0, 3, 2, 1] means A -> D -> C -> B -> A
```

Every city appears exactly once in the list. `route_distance` uses Euclidean
distance between consecutive coordinates and explicitly adds the edge from the
last city back to the first.

## Genetic Algorithm Steps

1. **Initial population:** Create random permutations with a manually
   implemented Fisher-Yates shuffle.
2. **Evaluation:** Calculate each route's total closed-tour distance. Shorter
   distance means a better candidate.
3. **Tournament selection:** Randomly sample candidate routes and copy the
   shortest one as a parent.
4. **Ordered crossover:** Preserve a segment from the first parent and fill the
   remaining positions in the second parent's order. A Boolean array records
   used cities so the child remains a valid permutation.
5. **Swap mutation:** With the configured probability, exchange two positions
   to introduce variation.
6. **Elitism:** Copy the best route found so far directly into the next
   generation so it cannot be lost.
7. **Best tracking:** Compare each generation's best route with the overall
   best and retain the shorter one.
8. **Presentation:** Rotate the final cyclic route so the first input city is
   printed first. Rotation does not change its length.

## Input and Output Design

The console program accepts:

- A built-in city set or at least three custom cities.
- Finite integer or decimal X and Y coordinates.
- Default genetic settings or custom population size, generation count,
  mutation rate, and integer random seed.

It displays:

- A table of input cities and coordinates.
- The best closed route found.
- Total route distance.
- All genetic settings used.
- A notice that the heuristic result is not guaranteed to be globally optimal.

Invalid numeric input, non-finite coordinates, and out-of-range settings are
rejected and requested again.

## Default Settings

| Setting | Value |
| --- | ---: |
| Population size | 60 |
| Generations | 150 |
| Mutation rate | 0.10 |
| Random seed | 2103 |

The fixed seed makes the built-in demonstration repeatable. Changing the seed
can explore a different sequence of candidate routes.

## Built-in Sample

| City | X | Y |
| --- | ---: | ---: |
| A | 0 | 0 |
| B | 0 | 4 |
| C | 3 | 4 |
| D | 3 | 0 |
| E | 1.5 | 2 |

With the default settings, the expected reproducible result is:

```text
A -> D -> C -> B -> E -> A
Total distance: 15.00
```

Equivalent rotations or reversals describe the same symmetric closed tour.

## Testing and Validation Evidence

| Test | Expected result | Actual result |
| --- | --- | --- |
| Three-city 3-4-5 triangle | Closed distance 12 | Pass |
| Unit square | Valid route with distance 4 | Pass |
| Return edge check | Last-to-first distance included | Pass |
| Ordered crossover | Complete permutation with no duplicates | Pass |
| Swap mutation | Complete permutation; original route unchanged | Pass |
| Same random seed twice | Identical route and distance | Pass |
| Route normalization | City index 0 appears first | Pass |
| Fewer than three cities | `ValueError` | Pass |
| Invalid GA settings | `ValueError` | Pass |
| `NaN` or infinite coordinate | `ValueError` | Pass |
| Custom console settings | Entered settings displayed accurately | Pass |

Correctness was checked by:

1. Comparing small triangle and square cases with manually calculated totals.
2. Confirming that crossover, mutation, and final results contain every city
   exactly once.
3. Confirming that route distance includes the return edge.
4. Repeating runs with the same seed to verify reproducibility.
5. Running invalid-input and console-flow automated tests.

Run the tests with:

```bash
python3 -m unittest -v problem3_tsp_genetic.test_genetic
```

## Complexity

Let:

- `n` be the number of cities.
- `P` be population size.
- `G` be number of generations.
- `T` be tournament size, fixed at 3 by default.

Route evaluation, Fisher-Yates shuffling, ordered crossover, mutation, and
best-route scanning are linear in `n`. The overall running time is
`O(G x P x T x n)`, which simplifies to `O(G x P x n)` for fixed tournament
size. Population storage is `O(P x n)`.

## Strengths and Limitations

Strengths:

- Works with larger search spaces without enumerating every possible tour.
- Uses modular, manually implemented genetic operators.
- Elitism prevents regression of the best-known solution.
- A fixed seed makes demonstrations and tests reproducible.
- Settings can be adjusted to explore quality-versus-runtime trade-offs.

Limitations:

- Does not guarantee a globally optimal route.
- Result quality depends on settings and the random search sequence.
- Larger populations and more generations require more processing time.
- Euclidean coordinates model symmetric distances only.

## Suggested Code Snippets

Include short extracts showing:

1. Closed-route distance calculation.
2. Ordered crossover and its used-city tracking.
3. Swap mutation.
4. Elitism and overall-best tracking in the generation loop.

Avoid placing the complete source file in the report body.

## Screenshot Checklist

- [ ] Built-in city table.
- [ ] Default route, distance, and settings.
- [ ] A run using custom GA settings.
- [ ] One invalid setting followed by a valid replacement.
- [ ] Automated test summary.

## AI Usage Guidance

Suggested declaration to adapt:

> Generative AI assisted with hardening the initial implementation, identifying
> validation cases, expanding automated tests, and organizing documentation.
> The group reviewed the route representation, selection, crossover, mutation,
> elitism, and distance calculation; manually checked small tours; ran the test
> suite; and confirmed that every returned chromosome was a valid route.
