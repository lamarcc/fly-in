*This project has been created as part of the 42 curriculum by celamarc.*

# Fly-in

## Description

Fly-in routes a fleet of drones from a start zone to an end zone across a network of connected zones, minimizing simulation turns while respecting zone occupancy, connection capacity, and per-zone-type movement costs (normal, priority, restricted, blocked).

The program parses a custom map file format, builds a graph model of the network, computes a path for every drone, and simulates their movement turn by turn until all drones are delivered. It is fully object-oriented and typesafe (flake8 + mypy compliant), and relies on no external graph library — the graph structures, pathfinding, and scheduling logic are entirely implemented from scratch.

## Instructions

```bash
make install       # uv sync — creates the venv and installs dependencies
make run             # uv run src/main.py — runs the simulation on a map
make debug           # runs the main script under pdb
make lint            # flake8 + mypy (standard flags)
make lint-strict      # flake8 + mypy --strict
make clean            # removes __pycache__ and .mypy_cache
```

The program reads a map file (see subject format), then outputs the movement of every drone turn by turn until all reach the end zone, with terminal and/or pygame visual feedback.

## Project structure

```
src/
├── parser/   # map parsing + custom error hierarchy
├── graph/    # Hub, Connection, Map — static graph model
├── engine/   # Drone, Simulation, pathfinding — runtime logic
├── render/   # terminal and pygame visualization
└── main.py
```

## Zone types & costs

| Type | Cost | Notes |
|---|---|---|
| normal | 1 turn | default |
| priority | 1 turn | preferred by the pathfinding tie-break |
| restricted | 2 turns | must arrive next turn, no mid-connection wait |
| blocked | — | excluded from the graph entirely |

## Algorithm choices

**Pathfinding**: a modified Dijkstra (dict-based, no heap), respecting per-zone costs as above. Priority zones use a separate internal comparison weight to break ties in their favor, as required by the subject; the turn count reported in the final output always uses the real cost (1 turn), never the internal tie-break weight.

**Multi-drone coordination**: drones are routed sequentially — each new drone's search accounts for the zone/connection reservations already made by previously routed drones (turn-indexed occupancy). A drone blocked by capacity waits in its current zone rather than idling mid-connection, since a connection can never be used to wait for a free slot in the destination zone.

**Complexity**: O(V²) per drone (linear-scan Dijkstra rather than a heap), O(D × V²) overall across D drones. This trades some performance on very large maps for simplicity and readability; a heap-based priority queue is a natural upgrade path if needed.

## Visual representation

- **Terminal**: colored `D<ID>-<destination>` output per turn, following the exact format required by the subject.
- **Pygame**: a window that visualizes the simulation turn by turn, showing the network of hubs and connections along with the current position of every drone.

## Example

```
nb_drones: 2
start_hub: start 0 0 [color=green]
end_hub: goal 4 0 [color=yellow]
hub: mid 2 0 [zone=priority color=cyan]
connection: start-mid
connection: mid-goal
```
Output:
```
D1-mid D2-mid
D1-goal D2-goal
```
Total: 2 turns.

## Resources

- 42 subject document (Fly-in, v1.6)
- Standard Dijkstra references (CLRS / graph theory coursework)
- Python `typing`/`mypy` docs, pygame official docs, `uv` documentation

### AI usage

AI was used for resuming various documentations used and for the README.
