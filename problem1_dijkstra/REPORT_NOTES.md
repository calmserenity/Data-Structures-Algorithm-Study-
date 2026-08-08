# Problem 1 Report Notes: Dijkstra's Shortest Path

Use these notes as source material for the Problem 1 and Testing and Validation
sections of the group report. Rewrite the explanations in the group's own words
after reviewing the implementation and greedy trace.

## Problem and Rationale

The program finds shortest routes from one starting location to every reachable
location in a weighted graph. Locations are vertices, routes are edges, and each
edge weight is a non-negative distance. The built-in example uses an illustrative
network of Kuala Lumpur landmarks; its distances are demonstration data rather
than a claim about exact road distances.

Dijkstra's algorithm is suitable because all route weights are non-negative. At
each stage it greedily selects the unvisited location with the smallest tentative
distance. No path through a more distant unvisited location can later reduce that
selected distance when every remaining edge has non-negative weight.

## Graph Representation

The graph is stored as an adjacency matrix:

- `graph[i][j]` is the distance from location `i` to location `j`.
- `None` means that no direct route exists.
- Diagonal entries are zero because a location is zero distance from itself.
- The custom-data interface creates a symmetric matrix for an undirected network.

An adjacency matrix makes every possible outgoing edge available through a
simple loop and keeps the manual implementation easy to explain.

## Algorithm

The program maintains three lists:

- `distances[v]`: shortest tentative distance currently known for vertex `v`.
- `previous[v]`: predecessor of `v` on the selected shortest path.
- `visited[v]`: whether the shortest distance to `v` has been finalized.

The main stages are:

1. Set every distance to infinity, except the starting vertex, which is zero.
2. Manually scan every unvisited vertex and select the one with the smallest
   tentative distance. This is the greedy choice.
3. Mark the selected vertex as visited.
4. Relax each outgoing edge. For a neighbour `v` of the selected vertex `u`:

   ```text
   candidate = distance[u] + weight[u][v]
   if candidate < distance[v]:
       distance[v] = candidate
       previous[v] = u
   ```

5. Record the selected vertex and successful improvements in the greedy trace.
6. Repeat until every reachable vertex has been visited.
7. Follow the predecessor list backwards to reconstruct a shortest path.

## How the Greedy Trace Demonstrates the Method

The trace displays the location selected at each stage, its finalized distance,
and every neighbour whose tentative distance improved. For the built-in sample,
the beginning of the trace is:

```text
Stage   Selected location           Final distance
1       KL Sentral                  0.00 km
        Improved neighbours: Pasar Seni=2.00 km,
        Merdeka Square=3.20 km, Mid Valley=4.00 km
2       Pasar Seni                  2.00 km
        Improved neighbours: Petaling Street=2.80 km,
        Masjid Jamek=3.20 km, Bukit Bintang=5.00 km
```

This is concise evidence of both the greedy selection and edge relaxation. It is
not a GUI animation; it is a formatted console summary of the algorithm's work.

## Input and Output Design

The console program offers:

- A built-in Kuala Lumpur landmark network for repeatable demonstrations.
- A custom undirected network with 2 to 20 uniquely named locations.
- Validation for route count, endpoints, duplicate routes, weights, and starting
  location.
- A menu to display one destination, all destinations, or the greedy trace.
- Clear path formatting using arrows and distances displayed in kilometres.
- Explicit `Unreachable` output where no route exists.

## Built-in Sample

Starting location: `KL Sentral`

Expected route to KLCC:

```text
KL Sentral -> Pasar Seni -> Masjid Jamek -> KLCC
Total distance: 6.30 km
```

The all-destinations table also displays the shortest path and total distance to
each of the ten sample locations.

## Testing and Validation Evidence

| Test | Expected result | Actual result |
| --- | --- | --- |
| KL Sentral to KLCC | Route through Pasar Seni and Masjid Jamek, 6.30 km | Pass |
| Start equals destination | One-vertex path with distance 0 | Pass |
| Unreachable destination | Infinity and empty reconstructed path | Pass |
| Shorter indirect route | Indirect route selected with distance 6 | Pass |
| Zero-weight edge | Valid shortest path uses the zero-weight edge | Pass |
| Large distance | Distance above ten million handled correctly | Pass |
| Empty graph | `ValueError` | Pass |
| Non-square matrix | `ValueError` | Pass |
| Invalid start indexes | `ValueError` | Pass |
| Negative edge | `ValueError` | Pass |
| Negative edge in disconnected component | `ValueError` | Pass |
| `NaN` or infinite edge | `ValueError` | Pass |
| Non-numeric edge | `ValueError` | Pass |
| Greedy trace order | Expected vertex selection order recorded | Pass |
| Greedy relaxations | Expected distance improvements recorded | Pass |
| Trace formatting | Selection rule and improvements displayed | Pass |
| Default location | Enter accepts the displayed default | Pass |
| Complete sample console run | Greedy trace displayed successfully | Pass |

Correctness was checked by:

1. Manually calculating paths on small graphs.
2. Comparing the KL Sentral to KLCC result with the edge weights in the matrix.
3. Confirming that the predecessor list reconstructs the expected path.
4. Confirming that each trace stage selects the smallest tentative distance.
5. Running validation, boundary, formatting, and console-flow tests.
6. Comparing 200 randomly generated graphs with an independent all-pairs
   shortest-path calculation during review.

Run the automated tests with:

```bash
python3 -m unittest -v problem1_dijkstra.test_dijkstra
```

## Complexity

For `V` locations:

- Time: `O(V^2)`. Each greedy stage manually scans all vertices, and the
  adjacency-matrix row scans all possible neighbours.
- Working memory excluding the graph: `O(V)` for distances, predecessors, and
  visited status.
- Graph storage: `O(V^2)` for the adjacency matrix.
- Optional trace storage: up to `O(V^2)` in the worst case because successful
  improvements are recorded for presentation.

## Strengths and Limitations

Strengths:

- Guarantees shortest paths when all edge weights are non-negative.
- Implements the greedy selection and relaxation manually.
- Returns both distances and reconstructable paths.
- Shows the greedy choice and successful relaxations in a readable trace.
- Supports built-in and custom networks, unreachable locations, and repeated
  destination queries.
- Uses no external graph or optimization libraries.

Limitations:

- Negative edge weights are not supported.
- An adjacency matrix uses more memory than an adjacency list for sparse graphs.
- The `O(V^2)` implementation is slower than a priority-queue version on large,
  sparse graphs, but it is clear and appropriate for the assignment's maximum of
  20 custom locations.
- Equal-distance alternatives use the first path encountered; another equally
  short route may exist.
- The built-in landmark distances are illustrative rather than live map data.

## Suggested Code Snippets

Include short extracts showing:

1. The manual scan that makes the greedy choice.
2. The edge-relaxation comparison and predecessor update.
3. Trace recording and formatted trace output.
4. Path reconstruction from the predecessor list.

Avoid pasting the entire program into the report body.

## Screenshot Checklist

- [ ] Built-in location menu and accepted default start.
- [ ] All-destinations route table.
- [ ] Greedy selection trace showing at least the first three stages.
- [ ] One custom network result.
- [ ] One unreachable destination.
- [ ] Automated test summary showing all Problem 1 tests passing.

## AI Usage Guidance

Suggested declaration to adapt:

> Generative AI assisted with reviewing input validation, expanding automated
> tests, designing the optional greedy trace, and organizing documentation. The
> group manually verified the selection and relaxation logic, calculated sample
> shortest paths, compared random non-negative graphs with an independent
> reference calculation, ran the test suite, and confirmed the displayed trace
> matches the algorithm's internal decisions.
