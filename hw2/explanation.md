# A document to explain the algorithm

## No.1 Create Hash Table from scratch with O(1) runtime
    # calculate_hash(key): hash number
            # I chose hash function as "hash +=ord(ch) * (i + 1)"
            # Since we need to make sure 'abs' and 'sba' falls into different slot/bucket, we keep track the index and multiply different number to each char
            # However I found out that "hash=hash*hash+ord(i)" is faster for thenperformance but I was not sure how to reason about this
    # Item class : key, value pair and pointer to next element in the bucket

    # HashTable class : bucket size, item_count, buckets capacity
        # put() : put into bucket
        # get() : serach from the table
        # delete() : delete from the table
        # size() : get size of the table


        # rehash() : In order to rehash when bigger than 70% of cap and smaller than 30% of cap
            # rehash_insert() : In order to reinsert every elements into new hash table but exclude size check and duplicate check from put()

## No.2 In databese, Whats the reasons why using O(log n) Tree is better than using O(1) hash table?
    # 1. While tree's time complexity is stable with O(log n), the hash table could be O(n) due to its collision or hash function.
    # 2. Altough the hash tabe is faster in searching one single data, Since database usually used often in searching the specific range of data, the tree structure is suitable for this condition.
    # 3. when space complexity is more important-> Tree has less memory than hash map
    # 4. tree is sequential -> faster to find similar data around and less expensive-> spatial locality

## + DS with always O(1) run time?
    # 1. trie-> tree but prefix of data as nodes
        # make a graph-> first char of string -> deeper-> get the whole string
        # string is constant -> time complexity -> O(len of string)->O(1)

## No.3 Design a cache that achieves the following operations with mostly O(1)
###     When a pair of <URL, Web page> is given, find if the given pair is contained in the cache or not
###     If the pair is not found, insert the pair into the cache after evicting the least recently accessed pair
    # cache data structure must be hash table to achieve O(1) 
    # but hash map is unordered.
    # For LRU cache, we need to store the order and update the least recently used item everytime we access-> use double Linked List to keep track of head and tail and update the pointer as you go
    # so when evicting -> we can just remove the least recently used pair
    

## No.4 Implement No3
    # LinkedList class : key, value, next, prev

    # LRUCache class : capacity, HashTable, head, tail, pointers to connext head and tail both way
        # put() : add into linked list
        # get() : search in linked list
        # delete() : delete the node
            # insert_2_tail() : insert into tail to make the node as most used node
            # remove() : remove the pointers

    