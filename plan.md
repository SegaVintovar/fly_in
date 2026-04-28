## Plan: Drone Navigation Project Structure

Build a clear, testable architecture in small phases: first make parsing and domain modeling correct, then add simulation and routing, then optimize behavior for harder maps. This plan also includes a reusable planning workflow so you can independently plan future projects.

**Steps**
1. Phase 1 - Lock Requirements and Map Rules
1.1 Capture rules as an explicit spec in `README` notes (success = all drones reach end hub, capacity = max simultaneous occupancy, connection direction from metadata, priority zones are preferred in pathfinding).
1.2 Define unsupported/unknown metadata behavior (warn + skip vs fail fast) to avoid parser ambiguity.
1.3 Create acceptance checklist per map tier (easy/medium/hard/challenger).
2. Phase 2 - Stabilize Core Domain (*depends on 1*)
2.1 Keep existing model classes in `fly_in.py` initially, but normalize attributes so they map 1:1 to map data: hub type, zone, occupancy, and connection capacity semantics.
2.2 Ensure `Map` owns graph state (hubs dictionary + adjacency list) and only one source of truth for drone positions.
2.3 Define invariants for each turn: no hub exceeds capacity, drone is on exactly one hub, and transitions only through valid connections.
3. Phase 3 - Finish Parsing Pipeline (*depends on 2*)
3.1 Complete parser flow in `parsing.py`: `parsing()`, `parse_hubs()`, `parse_connections()`, and metadata extraction.
3.2 Add validation errors with clear messages (missing start/end hub, malformed connection, unknown hub refs).
3.3 Parse directional behavior from metadata (or explicit default if metadata missing).
3.4 Produce a ready-to-run `Map` object consumed by `main.py`.
4. Phase 4 - Build Simulation + Routing (*depends on 3*)
4.1 Implement `find_valid_path()` in `Map` as initial BFS baseline (correctness first).
4.2 Implement `make_move()` as turn engine: compute candidate moves, apply capacity checks, resolve conflicts deterministically.
4.3 Add priority-zone weighting in route scoring (soft preference, not hard rule).
4.4 Wire execution flow in `main.py` so a map file runs end-to-end and prints turns/state.
5. Phase 5 - Testing Strategy (*parallel with 4.4 once parsing works; full pass depends on 4*)
5.1 Add parser-focused tests for map loading and metadata handling.
5.2 Add simulation tests for occupancy and conflict resolution.
5.3 Add end-to-end tests over map tiers: easy first, then medium/hard.
5.4 Add one regression test per bug found while solving harder maps.
6. Phase 6 - Refactor to Target Structure (*depends on 3 and can continue in parallel with 5*)
6.1 Move from flat files to modules only after behavior is stable: `src/models`, `src/parsing`, `src/simulation`, `src/pathfinding`.
6.2 Keep thin compatibility imports during migration to avoid breaking `main.py` and tests.
6.3 Update Makefile targets and test commands after migration.
7. Phase 7 - Optimization and Benchmarking (*depends on 4 and 5*)
7.1 Profile hard/challenger maps for bottlenecks in route selection/conflict handling.
7.2 Improve heuristics (capacity-aware routing, deadlock avoidance, priority-zone tie-breaks).
7.3 Track benchmark metrics per map (turn count, completion rate, runtime).

**Relevant files**
- `/mnt/c/Users/Laptop/study/fly_in_my_git/main.py` - orchestrator flow, CLI argument handling, run loop integration.
- `/mnt/c/Users/Laptop/study/fly_in_my_git/parsing.py` - complete parse pipeline (`parsing`, `parse_hubs`, `parse_connections`) and validation.
- `/mnt/c/Users/Laptop/study/fly_in_my_git/fly_in.py` - domain models (`Drone`, `Hub`, `Connection`, `Map`) and simulation/pathfinding methods (`make_move`, `find_valid_path`).
- `/mnt/c/Users/Laptop/study/fly_in_my_git/maps/README.md` - map format contract and rule clarifications.
- `/mnt/c/Users/Laptop/study/fly_in_my_git/maps/easy/*` - first acceptance set for correctness.
- `/mnt/c/Users/Laptop/study/fly_in_my_git/maps/medium/*` - dead-end and loop handling validation.
- `/mnt/c/Users/Laptop/study/fly_in_my_git/maps/hard/*` - capacity and routing stress tests.
- `/mnt/c/Users/Laptop/study/fly_in_my_git/maps/challenger/*` - final optimization benchmark.

**Verification**
1. Parse validation: run app against all easy maps and confirm map object creation succeeds without exceptions.
2. Rule validation: run targeted cases where hub occupancy reaches capacity; assert no move breaks occupancy invariant.
3. Behavior validation: confirm all drones reach an end hub for easy/medium maps before optimization work.
4. Regression validation: each fixed bug gains one reproducible test.
5. Performance validation: record turns/runtime on hard/challenger maps and compare after each optimization.

**Decisions**
- Included scope: structure plan, milestone order, testing strategy, and personal planning framework.
- Confirmed rules: all drones must reach end hub; capacity is simultaneous occupancy; connection direction depends on metadata; priority zones should be preferred in pathfinding.
- Excluded for now: advanced visualization UI and perfect-turn optimality proof.

**Further Considerations**
1. Direction metadata default when absent: Option A (bidirectional default, recommended), Option B (directed default), Option C (reject map).
2. Refactor timing: Option A (after parser+engine stable, recommended), Option B (immediate restructure), Option C (no restructure).
3. Optimization goal: Option A (good enough for all maps, recommended), Option B (min-turn focus), Option C (runtime focus only).

## Planning Framework You Can Reuse

1. Define outcome first: write one measurable success sentence (for this project: all drones reach end hub under map constraints).
2. Lock rules before coding: collect ambiguous rules and resolve them early (capacity, direction, zone behavior).
3. Model before algorithm: make sure domain objects can represent all constraints.
4. Build correctness baseline first: simple algorithm that works on easy cases.
5. Add tests by layer: parser -> engine -> end-to-end maps.
6. Refactor only after behavior is stable.
7. Optimize last with metrics, not guesses.

Use this checklist for any project:
- Problem statement
- Inputs/outputs
- Rules/constraints
- Core domain model
- Baseline implementation
- Verification strategy
- Refactor plan
- Optimization targets