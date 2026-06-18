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
def valid_edges(n, sorted_edges):
    # Input : length of cities, list of sorted(shortst top) edges 
    # -> Output: list of connected neighbor nodes => adjacency list

    # adjascency list to return
    adj=[]

    # Create empty adjacency list with one empty list per city
    for _ in range(n):
        adj.append([])
    
    # Union Find for n cities
    uf = UnionFind(n)

    # STEP 2 Connect the shortest path with Union Find

    # Traverse the edges list
    for distance, i, j in sorted_edges:

        # if these two cities not connected yet, and we want a path so we only allow at most 2 neighbours
        if uf.find(i)!=uf.find(j) and len(adj[i])<2 and len(adj[j])<2:
            # Connect -> add to each of adj list
            adj[i].append(j)
            adj[j].append(i)

            uf.union(i, j) # add these two cities components
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
    adj=valid_edges(len(cities), sorted_edges)

    # STEP 3 Repeat until connect all nodes -> Check if all connected
    tour=get_tour(adj, len(cities))

    return tour
    





# Resolve the intersection by swapping and get shorter tour
def two_opt(cities, tour):
    # STEP 1 Detect Crossing edge:
        # Check whether resolving crossing would shorten the original tour

    # STEP 2 Resolve intersection if needed



    



if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = greedy(read_input(sys.argv[1]))
    tour=two_opt(read_input(sys.argv[1]), tour)
    print_tour(tour)
