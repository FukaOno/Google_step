# Greedy + 2.0 opt + 2.5 opt

## solve() Structure
    SOLVE(cities)
        ↓
    Initialize parameters based on n
        ↓
    Build neighbor_lists (k-nearest neighbors) once
        ↓
    FOR each starting seed:
        ├─ Nearest neighbor greedy tour
        ├─ Local search pipeline (2-opt + 2.5-opt)
        ├─ Track as seed_best
        │
        ├─ KICK LOOP (up to max_kicks or time limit):
        │  ├─ Double bridge kick on seed_best
        │  ├─ Local search pipeline on kicked tour
        │  ├─ If improved:
        │  │  ├─ Update seed_best
        │  │  └─ Reset kick_count
        │  └─ Else:
        │     └─ Increment kick_count
        │
        └─ If seed_best beats global_best:
        └─ Update global_best

    Return global_best
