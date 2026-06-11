# Find shortest path

## Add code into find_shortest_path(self, start, goal)

### STEP 1 BFS into shortest path
    # shortest path -> min # of edges -> BFS always give to the shallowest path

    # start title and goal title is given
    # and self.titles = {id : title}
    # we need following:
    # start_id : start title
    # goal_id : goal title

    # traverse the self.title and get a new map with title : id
        ids={}
        for id, title in self.titles.items():
            # ids = {title : id }
            ids[title]=id
        
        # get the start id and goal id
        start_id = ids[start]
        goal_id = ids[goal]

        # if already reached to goal -> start id = goal id then return the path
        if start_id==goal_id:
            return [start_id]


        # prepare Queue with node
        q = collections.deque([start_id])

        # visited nodes : from None
        seen = {start_id : None}

        # Until Queue is not empty,
        while len(q) != 0:
            
            # dequeue the node
            node_id = q.popleft()

            # for neighbor of the node just visited,
            for neighbor_id in self.links[node_id]:
                if neighbor_id in seen:
                    continue
                
                # if not in seen yet, add the node
                # reached neighbor_id from node_id
                seen[neighbor_id]=node_id

                # put into queue if not visited yet and not goal yet
                if neighbor_id != goal_id:
                    q.append(neighbor_id)
                else:
                    # if reached to goal-> return the path 
                    path=[]
                    cur=goal_id

                    # we traverse backwards the path came from 
                    # Until we find the start node which come from node is None
                    while cur is not None:
                        path.append(cur)
                        cur = seen[cur]
                    
                    # since we backward tracked so reverse the path
                    path.reverse()
                    return path
        return None



