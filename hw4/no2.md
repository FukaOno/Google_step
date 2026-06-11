# Find 10 most popular pages with page rank

## Rules for page rank
    1. The node with more links have bigger pagerank
    2. The node that linked by bigger pagerank has bigger pagerank
    3. The node that linked by smaller distribution of links has bigger pagerank

## STEP 1 Initialize all node rank as 1.0
    pagerank ={}
    for id in self.titles:
        pagerank[id]=1.0


## STEP 2 Distribute the PageRank of each node evenly among its neighboring nodes

    # Initialize new pagerank map to update rank
    new_pagerank={}
    for id in self.titles:
        new_pagerank[id]=0.0
    
    # we need to distribute depending on the number of neighbors this node is connected to so
    # traverse each node and get distribution
    # distribution is rank of node / number of neighbors
    for id in self.titles:

        # skip pages with no outgoing links
        if len(self.links[id]) == 0:
                continue

        distribution= pagerank[id]/ len(self.links[id])

## STEP 3 Update the node's pagerank to sum of incoming pagerank
    # Update the page rank to new pagerank map

    for distribution_id in self.links[id]:
            new_pagerank[distribution_id]+=distribution

## STEP 4 Repeat 2&3 until it converges
    # converges when : sum(new_pagerank[i] - old_pagerank[i])**2 < 0.01

    

## STEP 5 Print the top 10
    sorted_pages = sorted(pagerank, key=lambda id: pagerank[id], reverse=True)
    for id in sorted_pages[:10]:
        print(self.titles[id], pagerank[id])


## Issue: Could not check for large.txt file since it was too big and too slow to run
