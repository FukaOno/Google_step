# TSP with Greedy Algo and 2-opt


## Greedy -> Choose the shortest path between two nodes first and connect all as you go

### STEPS for Greedy Algorithm
    # STEP 1 Traverse all edges and sort by distance
    # STEP 2 Connect the shortest path-> Union Find
    # STEP 3 Repeat until connect all nodes 

### Functions 
    # 1. Distance helper function
        sqrt((x1-x2)^2 + (y1-y2)^2)

    # 2. Union Find
        # In order to avoid creating circles or partial paths, get parent of node, merge two nodes witout cycles
        
        # Check if two cities already connected or not
        # find(x) => Find the parent/root of x

        # Merge two components into one
        # union(x, y) => Merge the two connected paths containing x and y

    # 3. get_sorted_edge_list(cities)=> STEP 1
    # 4. valid_edges(n, sorted_edges)=> STEP 2
    # 5. get_tour(adj, n) => STEP 3
    # 6. greedy(cities) => Main function
        
        def greedy(cities):

            # STEP 1 Traverse all edges and sort by distance
            sorted_edges = get_sorted_edge_list(cities)

            # STEP 2 Connect the shortest path-> Union Find
            adj=valid_edges(len(cities), sorted_edges)

            # STEP 3 Repeat until connect all nodes -> Check if all connected
            tour=get_tour(adj, len(cities))

            return tour



## 2-opt -> When two routes are crossing, we resolve the cross and can get shorter routes
    # STEP 1 Check whether resolve crossing would shorten the original tour
    # STEP 2 Resolve intersection if needed



## Combine these operations
    # Greedy-> opt -> print

