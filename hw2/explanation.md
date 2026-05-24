# A document to explain the algorithm

## No1 Create Hash Table from scratch with O(1) runtime
    # implemented put(), get(), delete()
    # rehash() for rehashing when bigger than 70% of cap and smaller than 30% of cap
    # TO FIX: odd number hash, find better hash function, error in check_size()

## No2 In databese, Whats the reasons why using O(log n) Tree is better than using O(1) hash table?
    # 1. While tree's time complexity is stable with O(log n), the hash table could be O(n) due to its collision or hash function.
    # 2. Altough the hash tabe is faster in searching one single data, Since database usually used often in searching the specific range of data, the tree structure is suitable for this condition.

## No3 Design a cache that achieves the following operations with mostly O(1)
###     When a pair of <URL, Web page> is given, find if the given pair is contained in the cache or not
###     If the pair is not found, insert the pair into the cache after evicting the least recently accessed pair
    # cash data structure must be hash table to achieve O(1) 
    # but hash map is unordered.
    # For LRU cache, we need to store the order and update the least recently used item everytime we access-> use double Linked List to keep track of head and tail and update the pointer as you go
    # so when evicting -> we can just remove the least recently used pair
    

## No4 Implement No3
    # the code is in lru_cache.py
    # TO FIX: configure with the hash_table.py instead of python dict


    