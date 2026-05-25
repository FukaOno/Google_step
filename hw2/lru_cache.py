from hash_table import HashTable

class LinkedListNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.map = HashTable()
        # initialize head -> <= tail
        self.head=LinkedListNode(-1, -1)
        self.tail = LinkedListNode(-1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    
    def put(self, key, value):

        node, found = self.map.get(str(key))
        if found:
            self.remove(node) # remove from least recently used
            self.map.delete(str(key))

        # create a new node
        new = LinkedListNode(key, value)
        self.map.put(str(key), new)
        self.insert(new) # add to the most recently

        # check if the capacity is available
        # if not available -> evict : remove the least
        if self.map.size() > self.capacity:
            least = self.head.next
            self.remove(least)
            self.map.delete(str(least.key)) # delete from hash map 
            
    
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
         # we need to update to most recently accessed
        node, found = self.map.get(str(key))
        if found:
            self.remove(node) # remove from least recently used
            self.insert(node) # add to the most recent
            return (node.value, True)
        else:
            return (None, False)
        
    
    def delete(self, key):
        old, found = self.map.get(str(key))
        if not found:
            return False
        else:
            # delete and update pointer
            self.remove(old)
            self.map.delete(str(key))
            return True
            

        
