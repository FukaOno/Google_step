# Best Fit malloc

## The difference with First Fit malloc:
    # First Fit : only look for block where metadata->size >= size
    # Best Fit : look for entire free list and look for best fit considering size

## Steps for Best Fit :
    # Pointer : To save best fit so far
    # STEP 1 : Travese all the free blocks✅
    # STEP 2 : Check if the size big enough for the required size✅
    # STEP 3 : Check if this smaller than best-fit so far or not✅
    # STEP 4 : After loop, check if best fit acquired or not
        # If acquired : done✅
        # If not : use mmap_from_system()✅

# Freelist Bin

## The difference with my_heap_t
    # We maintain multiple free lists, where each list only holds free blocks of a specific size range
    # The maximum size is 4000 bytes and everything is a multiple of 8-> Group them tgt

## Steps for Freelist Bin with 4 bins-array:
    # STEP 1 : Define an array of free heads, one for each bin✅
    # STEP 2 : Define helper for a way to look at a size and determine which bin index it belongs to✅
    # STEP 3 : Update functions to match the index instead of global one list✅
        # my_add_to_free_list and my_remove_from_free_list
    # STEP 4 : Clear out the dummy and initialize every bin head in new free_heads✅
    # STEP 5 : Update my_malloc
        # 1. Find starting bin✅
        # 2. Find best fit from start_bin✅
    
# Return empty page
    # Case 1 : if a user allocates exactly one large chunk and frees it
        # -> Return empty page 
        
    # Case 2 : if a 4096-byte page was split into smaller blocks -> Check neighbors
        # -> Merge Right Vacant Region

## Steps for returning empty page

    # STEP 1 : Update my_free to check the size✅
    # STEP 2 : if that Merged block's size is 4096 - sizeof(my_metadata_t), return to system by calling munmap_to_system✅

        // #Return Page STEP 1 : Update my_free to check the size
        size_t full_page_payload_size = 4096 - sizeof(my_metadata_t);

        if (metadata->size == full_page_payload_size) {
            
            // #Return Page STEP 2 : if that Merged block's size is 4096 - sizeof(my_metadata_t), return to system by calling munmap_to_system
            munmap_to_system(metadata, 4096);
        }else {
            // If it's not a full page, add it to its proper size bin
            my_add_to_free_list(metadata);
        }

# Merge Right Vacant Region

## Steps for Merge
    # STEP 1 : Calculate the right neighbor's target address✅
        # Metadata header -> (char *)metadata
        # The size of tracking header-> sizeof(my_metadata_t)
        # The size (in bytes) of the usable user allocation payload space -> metadata->size

    # STEP 2 : Scan all bins to see if any free block matches our right neighbor's address✅
    # STEP 3 : Isolate the neighbor✅
        # pull it out of its current linked list using my_remove_from_free_list(right_neighbor, right_neighbor_prev). # This prevents the bin's linked list chain from snapping.
    # STEP 4 : Merge by increasing size (add right neighbor's size to current size)✅
