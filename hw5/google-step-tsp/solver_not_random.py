import math
import sys

from common import print_tour, read_input

# helpers for greedy
def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

class UnionFind:
    # In order to avoid creating circles or partial paths
    # Check if two cities already connected or not
    # Merge two components into one

    def __init__(self, size):
        # parent is the root of the connected cities
        self.parent = list(range(size))
    
    def find(self, x):
        # Find the parent/root of x

        # Until it lands on the node that points to itself
        while self.parent[x]!=x:

            # Keep climbing up to find the parent of x
            x=self.parent[x]
        return x
    
    def union(self, x, y):
        # Merge the two connected paths containing x and y

        # STEP 1 Find the root of x
        root_x=self.find(x)

        # STEP 2 Find the root of y
        root_y=self.find(y)

        # STEP 3 Make root of x point to root of y
        # -> x component merged to y component
        self.parent[root_x]=root_y



def get_sorted_edge_list(cities):
    # STEP 1 Traverse all edges and sort by distance
    # Input: cities
    # Output: return list of sorted edges

    # Get number of cities
    cities_length=len(cities)

    # egdes list to return
    edges=[]

    # get all distances from nodes to nodes
    for i in range(cities_length):
        for j in range(i+1, cities_length):
            # get distance of node i and node j
            edges.append((distance(cities[i], cities[j]), i, j))
    
    edges.sort() # shortest on top
    return edges


# Get Adj list of nodes
def valid_edges(cities, sorted_edges):
    # Input : list of cities, list of sorted(shortst top) edges 
    # -> Output: list of connected neighbor nodes => adjacency list

    # adjascency list to return
    adj=[]

    # Create empty adjacency list with one empty list per city
    for _ in range(len(cities)):
        adj.append([])
    
    # Union Find for all cities
    uf = UnionFind(len(cities))

    # STEP 2 Connect the shortest path with Union Find

    # Traverse the edges list
    for distance, i, j in sorted_edges:

        # if these two cities not connected yet, and we want a path so we only allow at most 2 neighbours
        if uf.find(i)!=uf.find(j) and len(adj[i])<2 and len(adj[j])<2:
            # Connect -> add to each of adj list
            adj[i].append(j)
            adj[j].append(i)

            uf.union(i, j) # add these two cities components

    # STEP 3 Stitch together any remaining disjoint fragments
        # After the loop above, adj may form several separate path
        # fragments instead of one single path through all n cities
    while True:
        endpoints=[] # all city with degree < 2 (0 or 1 neighbors)

        for city in range(len(cities)):
            if len(adj[city])<2: # all city with degree < 2 (0 or 1 neighbors)
                endpoints.append(city)

        # In order to check if all paths connected or not, 
        # get all paths' root by find() and put into unique set
        roots=set()

        for city in endpoints:
            roots.add(uf.find(city))
        
        if len(roots)<=1:
            # we connected all paths
            break
        
        # Find closest pair of endpoints in different root
        closest = None
        for a in range(len(endpoints)):
            for b in range(a + 1, len(endpoints)):
                city_a, city_b = endpoints[a], endpoints[b]
                if uf.find(city_a) == uf.find(city_b):
                    # same roots already so skip
                    continue

                # otherwise, get distance
                d = distance(cities[city_a], cities[city_b])

                # Compare with cloest
                if closest is None or d < closest[0]:
                    closest = (d, city_a, city_b)

        # Connect the closest city with different root
        _, city_a, city_b = closest
        adj[city_a].append(city_b)
        adj[city_b].append(city_a)
        uf.union(city_a, city_b)
    return adj


# Build up tour from adj list
def get_tour(adj, n):
    # Input : list of adj nodes, length of cities 
    # Output: list of nodes-> tour

    # the result path
    tour=[0]

    cur_city=0 # current city index
    prev_city=-1 # prev city index

    for _ in range(n-1):
        # Traverse edges
        for nei in adj[cur_city]:

            # if neighbor is not a prev city then
            if nei!=prev_city:

                # update prev and cur
                prev_city=cur_city
                cur_city=nei

                # since we reached all neighbors-> break
                break

        tour.append(cur_city)
    return tour




# Choose the shortest path between two nodes first and connect all as you go
def greedy(cities):

    # STEP 1 Traverse all edges and sort by distance
    sorted_edges = get_sorted_edge_list(cities)

    # STEP 2 Connect the shortest path-> Union Find
    adj=valid_edges(cities, sorted_edges)

    # STEP 3 Repeat until connect all nodes -> Check if all connected
    tour=get_tour(adj, len(cities))

    return tour
    





# STEP 1 Detect Crossing edge:
def is_shorter(cities, tour, i, j):

    # 1-> 2 connected, inorder to get actual coordinate (x, y) => require index in cities
    city_1=tour[i]
    city_2=tour[i+1]

    # 3-> 4 connected, inorder to get actual coordinate (x, y) => require index in cities
    city_3=tour[j]
    city_4=tour[(j+1)%len(cities)] 
    # In order to prevent "Index out of range" error, and correctly back to index 0

    #  STEP 1 Compare length
    cur_edge_length=distance(cities[city_1], cities[city_2])+distance(cities[city_3], cities[city_4])
    
    # resolve crossing by swapping => connect 1-> 3, 2-> 4
    new_edges_length=distance(cities[city_1], cities[city_3])+distance(cities[city_2], cities[city_4])


    # STEP 2 Check whether resolving crossing would shorten the original tour
    return cur_edge_length > new_edges_length


# STEP 2 Resolve intersection
def resolve_crossing(tour, i, j):
    # Since we want to swap A->B and C->D to
    # A-> C and B-> D

    # We require reversing B and C position
    # Once we found the specific range of tour is shorter 
    # -> we perform reverse of cities in between

    # Take i+1 to j amount of tour and reverse them
    tour[i+1:j+1]=tour[i+1:j+1][::-1]


# Resolve the intersection by swapping and get shorter tour
def two_opt(cities, tour):
    
    # i and j are two edges
    for i in range(len(cities)-1):
        for j in range(i+2, len(cities)): # In order to not share two edges tour[i]->tour[i+1], start j from i+2
                
                # STEP 1 Detect Crossing edge:
                # Check whether resolving crossing would shorten the original tour
                if is_shorter(cities, tour, i, j):

                    # STEP 2 Resolve intersection if needed
                    resolve_crossing(tour, i, j)
    return tour


def solve(cities):
    tour = greedy(cities)
    tour = two_opt(cities, tour)
    return tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = greedy(read_input(sys.argv[1]))
    tour=two_opt(read_input(sys.argv[1]), tour)
    print_tour(tour)
