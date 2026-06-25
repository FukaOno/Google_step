import math
import sys
import time
import random

from common import print_tour, read_input

def distance(city1, city2):
    return math.hypot(city1[0] - city2[0], city1[1] - city2[1])

def tour_length(cities, tour):
    total = 0.0
    n = len(tour)
    
    # Traverse tour and get total distance
    for i in range(n):
        total += distance(cities[tour[i]], cities[tour[(i + 1) % n]])
    return total

# greedy (nearest neighbours)
def nearest_neighbor_tour(cities, start_city):
    n = len(cities)

    # Creates a list of n booleans, tracks which cities have been visited
    visited = [False] * n

    # STEP 1 : Start at a city
    tour = [start_city]
    visited[start_city] = True
    current = start_city

    # STEP 2 : move to the nearest unvisited city
    for _ in range(n - 1): # n-1 remaining 

        next_city = None # nearest unvisited city
        best_dist = float('inf') # tracks shortest distance found
        curr_loc = cities[current]
        
        for candidate in range(n): # find nearest

            if visited[candidate]:
                continue # skip visited

            d = distance(curr_loc, cities[candidate])

            # if this candidate is closer than the prev shortest, update
            if d < best_dist:
                best_dist = d
                next_city = candidate
                
        if next_city is None: # no unvisited city was found, exit the loop
            break

        visited[next_city] = True
        tour.append(next_city)
        current = next_city
    return tour

# For each city, pre-compute the k-nearest cities
def build_neighbor_lists(cities, k=50):
    n = len(cities)
    neighbor_lists = []

    # STEP 1 : Traverse all city
    for i in range(n):
        dists = [] # STEP 2 : Store distance from city i to all other cities
        for j in range(n):
            if i != j:
                dists.append((distance(cities[i], cities[j]), j))

        # STEP 3 : Sort the list by distance
        dists.sort(key=lambda x: x[0])
        # STEP 4 : Take first k cities from sorted list, appends to neighbour_lists
        neighbor_lists.append([j for _, j in dists[:k]])

    return neighbor_lists

# 2-opt
def fast_two_opt(cities, tour, neighbor_lists, pos, time_limit, start_time):
    
    n = len(tour)
    improved = True # flag to track if any improvement was found in the current iteration
    
    while improved:

        # To prevent running forever, set time limit, if exceeded-> break
        if time.time() - start_time > time_limit:
            break

        improved = False
        
        for i in range(n): # Traverse all position in tour
            if time.time() - start_time > time_limit:
                break
            
            # STEP 1 : Get two city pos and distance between them
            u = tour[i] # current city at pos i
            v = tour[(i + 1) % n] # next city, wraps around at the end
            dist_uv = distance(cities[u], cities[v]) # precompute distance between u and v
            
            # Optimization : Check only k nearest neighbors of u -> O(k * n)
            for w in neighbor_lists[u]:
                j = pos[w]
                if j == i or j == (i + 1) % n or j == (i - 1) % n: 
                    # w is same as u, w is the same as v, w is adj to u-> skip
                    continue
                
                z = tour[(j + 1) % n] # city after w in the tour

                old_dist = dist_uv + distance(cities[w], cities[z]) # u->v and w->z
                new_dist = distance(cities[u], cities[w]) + distance(cities[v], cities[z]) # u->w and v->z
                
                # STEP 2 : if new_dist is shorter-> swap
                if new_dist + 1e-9 < old_dist: # In order to handle floating-point comparison, add 1e-9
                
                    idx_v = (i + 1) % n # pos of v
                    idx_w = j # pos of w
                    
                    # STEP 3 : Perform swap with reversed()
                    if idx_v < idx_w: # segment is between v and w
                        tour[idx_v : idx_w + 1] = reversed(tour[idx_v : idx_w + 1])
                    else: # segment wraps around-> reverse the middle part
                        tour[idx_w + 1 : idx_v] = reversed(tour[idx_w + 1 : idx_v])
                    
                    # Update position mapping
                    for idx in range(n):
                        pos[tour[idx]] = idx
                        
                    # Mark improvements in the neighbor loop
                    improved = True
                    break
            
            # break the position loop if improved-> start while loop from 0
            if improved:
                break
    return tour

# 2.5-opt Node Insertion
def fast_two_dot_five_opt(cities, tour, neighbor_lists, pos, time_limit, start_time):
    n = len(tour)
    improved = True
    
    while improved:
        if time.time() - start_time > time_limit:
            break
        improved = False
        
        for i in range(n):
            if time.time() - start_time > time_limit:
                break
            
            # ...-> prev_u -> u -> next_u -> ...
            u = tour[i]
            prev_u = tour[(i - 1) % n]
            next_u = tour[(i + 1) % n]
            
            # STEP 1 : Pre-Calculate removal cost
            # prev_u-> u -> next_u
            removed_dist = distance(cities[prev_u], cities[u]) + distance(cities[u], cities[next_u])
            # prev_u-> next_u
            inserted_saved = distance(cities[prev_u], cities[next_u])
            
            # Cost saved by removing u from current pos
            base_delta = inserted_saved - removed_dist
            
            # Optimization : Check only k nearest neighbors of u -> O(k * n)
            for v in neighbor_lists[u]:
                j = pos[v]
                if j == i or j == (i - 1) % n:
                    # v is the same as u or v is prev_u
                    continue
                
                # STEP 2 : Calculate Cost of Inserting at this pos
                next_v = tour[(j + 1) % n]
                # v-> u->next_v
                added_dist = distance(cities[v], cities[u]) + distance(cities[u], cities[next_v])
                # v-> next_v
                current_edge_dist = distance(cities[v], cities[next_v])
                
                # Cost of inserting u at this position
                delta = base_delta + (added_dist - current_edge_dist)
                
                # if delta is less than 0 -> this new tour is shorter
                if delta + 1e-9 < 0:

                    # remove city from tour
                    city_to_move = tour.pop(i)

                    # all city after i shift left by 1
                    insert_pos = j if j < i else j - 1

                    # insert u after j
                    # v-> u -> next_v
                    tour.insert((insert_pos + 1) % len(tour), city_to_move)
                    
                    for idx in range(n):
                        pos[tour[idx]] = idx

                    improved = True
                    break

            if improved:
                break

    return tour

# Divide routes into 4 seg-> Replace 
def double_bridge_kick(tour, pos):

    n = len(tour)

    if n < 8: # if fewer than 8, no root to create 4 segments
        return tour
    
    # 4 random seg to ensure cut pos are spread out across entire tour
    size = n // 4

    # Quarter 1: positions 1 to size
    # Quarter 2: positions (size+1) to 2*size
    # Quarter 3: positions (2*size+1) to 3*size
    # Quarter 4: positions (3*size+1) to n-1

    p1 = random.randint(1, size)
    p2 = random.randint(p1 + 1, p1 + size)
    p3 = random.randint(p2 + 1, p2 + size)
    
    # 4 segs a->b->c->d
    a = tour[:p1]
    b = tour[p1:p2]
    c = tour[p2:p3]
    d = tour[p3:]
    
    #new 
    new_tour = a + d + c + b

    # Update position mapping
    for idx, city in enumerate(new_tour):
        pos[city] = idx
    return new_tour

def local_search_pipeline(cities, tour, neighbor_lists, time_limit, start_time):
    # Repeat 2-opt and 2.5-opt until no improvements find
    n = len(tour)
    pos = [0] * n
    for idx, city in enumerate(tour):
        pos[city] = idx
        
    last_len = tour_length(cities, tour)
    
    while time.time() - start_time < time_limit:
        # STEP 1 : Run 2-opt until no improvement
        tour = fast_two_opt(cities, tour, neighbor_lists, pos, time_limit, start_time)
        # STEP 2 : Run 2.5-opt until no improvement
        tour = fast_two_dot_five_opt(cities, tour, neighbor_lists, pos, time_limit, start_time)
        
        curr_len = tour_length(cities, tour)

        if last_len - curr_len < 1e-2: # Stop if improvement becomes negligible (<0.01 units)
            break

        last_len = curr_len
        
    return tour, pos

def solve(cities):
    n = len(cities)

    # Handle edge cases
    if n == 0:
        return []
    if n == 1: 
        return [0]
    if n == 2: # two cities -> only one possible tour
        return [0, 1]
    
    global_start_time = time.time() # set total time limit
    random.seed(42) # fixed radom seed : when same input -> same random choices
    
    # Depending on the city size, set different parameter
    if n >= 8000:     # Large problems
        k_neighbors = 40
        seeds = [0, n // 2] # test two differen starting points, 0 and middle
        time_per_seed = 25.0
        max_kicks = 3
    elif n >= 2000:  # Medium problems
        k_neighbors = 60
        seeds = [0, n // 4, n // 2, 3 * n // 4]
        time_per_seed = 12.0
        max_kicks = 5
    else:             # Small problems
        k_neighbors = min(50, n - 1)
        seeds = list(range(0, n, max(1, n // 12)))
        time_per_seed = 3.0
        max_kicks = 8

    # STEP 1 : Optimization : Build neighbor lists once
    neighbor_lists = build_neighbor_lists(cities, k=k_neighbors)
    
    # Initialize shortest solution 
    best_tour = None
    best_length = float('inf')
    
    # STEP 2 : Loop over multiple seeds
    for seed in seeds:
        if time.time() - global_start_time > 55.0:
            break
            
        # STEP 3 : Greedy Nearest Neighbor
        tour = nearest_neighbor_tour(cities, seed)
        
        # STEP 4 : First Local Search (2-opt + 2.5 opt)
        tour, pos = local_search_pipeline(cities, tour, neighbor_lists, time_per_seed, time.time())
        curr_len = tour_length(cities, tour)
        
        # Initialize seed level best
        seed_best_tour = tour[:]
        seed_best_len = curr_len
        
        # STEP 5 : Local Search Kick Loop 
        seed_start = time.time()
        kick_count = 0
        while time.time() - seed_start < time_per_seed and kick_count < max_kicks:
            # Time allocated for this seed exhausted
            # Maximum number of consecutive unsuccessful kicks reached-> break

            # STEP 6 : Double Bridge Kick
            kicked_tour = double_bridge_kick(seed_best_tour[:], pos)

            # STEP 7 : Apply Local Search to Kicked Tour
            optimized_tour, pos = local_search_pipeline(cities, kicked_tour, neighbor_lists, time_per_seed, seed_start)
            
            opt_len = tour_length(cities, optimized_tour)

            # Update Shortest or increment kick counter
            if opt_len < seed_best_len:
                seed_best_len = opt_len
                seed_best_tour = optimized_tour[:]
                kick_count = 0 # if Improved -> reset the counter
            else:
                kick_count += 1
        
        # Update Global Shortest
        if seed_best_len < best_length:
            best_length = seed_best_len
            best_tour = seed_best_tour[:]
            
    return best_tour

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cities = read_input(sys.argv[1])
        tour = solve(cities)
        print_tour(tour)