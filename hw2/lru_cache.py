class LinkedListNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.map = {} # hash map for saving the node : value pair-> update to the hash_table.py
        # initialize head -> <= tail
        self.head=LinkedListNode(-1, -1)
        self.tail = LinkedListNode(-1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    
    def put(self, key, value):
        if key in self.map:
            old = self.map[key]
            self.remove(old) # remove from least recently used

        # create a new node
        node = LinkedListNode(key, value)
        self.map[key]=node
        self.insert(node) # add to the most recently

        # check if the capacity is available
        # if not available -> evict : remove the least
        if len(self.map) > self.capacity:
            least = self.head.next
            self.remove(least)
            del self.map[least.key] # delete from hash map 
    
    def remove(self, node):
        # remove from left (head)-> update the pointer
        node.prev.next = node.next
        node.next.prev=node.prev
    
    def insert(self, node):
        # insert at the right (tail)-> update the pointer
        previous_end = self.tail.prev
        previous_end.next = node # new node as the tail
        node.prev = previous_end
        node.next = self.tail
        self.tail.prev = node

    
    def get(self, key):
        if key in self.map:
            # we need to update to most recently accessed
            node = self.map[key]
            self.remove(node) # remove from least recent
            self.insert(node) # add to the most recent
            return (node.value, True)
        else:
            return (None, False)
        
    
    def delete(self, key):
        if key not in self.map:
            return False
        else:
            # delete and update pointer
            old = self.map[key]
            del old
            old.prev.next = old.next
            old.next.prev=old.prev
            

        
