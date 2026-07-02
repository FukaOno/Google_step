//
// >>>> malloc challenge! <<<<
//
// Your task is to improve utilization and speed of the following malloc
// implementation.
// Initial implementation is the same as the one implemented in simple_malloc.c.
// For the detailed explanation, please refer to simple_malloc.c.

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//
// Interfaces to get memory pages from OS
//

void *mmap_from_system(size_t size);
void munmap_to_system(void *ptr, size_t size);

//
// Struct definitions
//

typedef struct my_metadata_t {
  size_t size;
  struct my_metadata_t *next;
} my_metadata_t;

typedef struct my_heap_t {
  // #Freelist Bin STEP 1 : Define an array of free heads, one for each bin
  my_metadata_t *free_heads[4];
} my_heap_t;

//
// Static variables (DO NOT ADD ANOTHER STATIC VARIABLES!)
//
my_heap_t my_heap;

//
// Helper functions (feel free to add/remove/edit!)
//

// #Freelist Bin STEP 2 : Define helper for a way to look at a size 
                          // and determine which bin index it belongs to
int get_bin_index(size_t size) {
  if (size <= 64) return 0;
  if (size <= 256) return 1;
  if (size <= 1024) return 2;
  return 3; 
}

// #Freelist Bin  STEP 3 : Update functions to match the index instead of global one list

void my_add_to_free_list(my_metadata_t *metadata) {
  assert(!metadata->next);

  int index = get_bin_index(metadata->size);
  metadata->next = my_heap.free_heads[index];
  my_heap.free_heads[index] = metadata;

}

void my_remove_from_free_list(my_metadata_t *metadata, my_metadata_t *prev) {
  if (prev) {
    prev->next = metadata->next;
  } else {
    int index = get_bin_index(metadata->size);
    my_heap.free_heads[index] = metadata->next;
  }
  metadata->next = NULL;
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
// #Freelist Bin  STEP 4 : Clear out the dummy and initialize every bin head in new free_heads
void my_initialize() {
  for (int i = 0; i < 4; i++) {
    my_heap.free_heads[i] = NULL;
  }
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
void *my_malloc(size_t size) {

  // #Freelist Bin STEP 5-1 : Find starting bin
  int start_bin = get_bin_index(size);

  my_metadata_t *best=NULL;
  my_metadata_t *best_prev = NULL;

  // #Freelist Bin STEP 5-2 : Find best fit from start_bin
  for (int i = start_bin; i < 4; i++) {
    my_metadata_t *metadata = my_heap.free_heads[i];
    my_metadata_t *prev = NULL;
  
  
  // #Best-Fit STEP 1 : Travese all the free blocks
    while (metadata) {

      // #Best-Fit STEP 2 : Check if the size big enough for the required size
      if (metadata->size>=size){

        // #Best-Fit STEP 3 : Check if this smaller than best-fit so far or not
        if (!best || metadata->size < best->size){
          // If it is, update pointer

          best=metadata;
          best_prev=prev;
        }

        // If it's a perfect fit, it can't get any better. Stop looking!
        if (metadata->size == size) {
          break;
        }

      }
      prev = metadata;
      metadata = metadata->next;
    }

    if (best) {
      break;
    }

  }

  // now, metadata points to the first free slot
  // and prev is the previous entry.

  // #Best-Fit STEP 4 : After loop, check if best fit acquired or not
      // If not : use mmap_from_system()
  if (!best) {
    // There was no best free slot available. We need to request a new memory region
    // from the system by calling mmap_from_system().
    
    size_t buffer_size = 4096;
    my_metadata_t *new = (my_metadata_t *)mmap_from_system(buffer_size);
    new->size = buffer_size - sizeof(my_metadata_t);
    new->next = NULL;
    // Add the memory region to the free list.
    my_add_to_free_list(new);
    // Now, try my_malloc() again. This should succeed.
    return my_malloc(size);
  }
  // If acquired : Use the best block found
  my_metadata_t *metadata = best;
  my_metadata_t *prev = best_prev;

  // |ptr| is the beginning of the allocated object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  void *ptr = metadata + 1;
  size_t remaining_size = metadata->size - size;
  // Remove the free slot from the free list.
  my_remove_from_free_list(metadata, prev);

  if (remaining_size > sizeof(my_metadata_t)) {
    // Shrink the metadata for the allocated object
    // to separate the rest of the region corresponding to remaining_size.
    // If the remaining_size is not large enough to make a new metadata,
    // this code path will not be taken and the region will be managed
    // as a part of the allocated object.
    metadata->size = size;
    // Create a new metadata for the remaining free slot.
    //
    // ... | metadata | object | metadata | free slot | ...
    //     ^          ^        ^
    //     metadata   ptr      new_metadata
    //                 <------><---------------------->
    //                   size       remaining size
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    // Add the remaining free slot to the free list.
    my_add_to_free_list(new_metadata);
  }
  return ptr;
}

// This is called every time an object is freed.  You are not allowed to
// use any library functions other than mmap_from_system / munmap_to_system.
void my_free(void *ptr) {
  // Look up the metadata. The metadata is placed just prior to the object.
  //
  // ... | metadata | object | ...
  //     ^          ^
  //     metadata   ptr
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  metadata->next = NULL;

  // ##Merge Right STEP 1 : Calculate the right neighbor's target address
  char *my_tail = (char *)metadata + sizeof(my_metadata_t) + metadata->size;

  my_metadata_t *right_neighbor = NULL;
  my_metadata_t *right_neighbor_prev = NULL;

  // #Merge Right STEP 2 : Scan all bins to see if any free block matches our right neighbor's address
  for (int i = 0; i < 4; i++) {
    my_metadata_t *curr = my_heap.free_heads[i];
    my_metadata_t *prev = NULL;

    // Check each free block's linked list
    while (curr) {
      if ((char *)curr == my_tail) {
        right_neighbor = curr;
        right_neighbor_prev = prev;
        break;
      }
      prev = curr;
      curr = curr->next;
    }
    if (right_neighbor) break;
  }
  
  
  if (right_neighbor) {
    // #Merge Right STEP 3 : Isolate the neighbor
    my_remove_from_free_list(right_neighbor, right_neighbor_prev);

    // #Merge Right STEP 4 : Merge by increasing size (add right neighbor's size to current size)
    metadata->size += sizeof(my_metadata_t) + right_neighbor->size;
  }
    
  // #Return Page STEP 1 : Update my_free to check the size
  size_t full_page_payload_size = 4096 - sizeof(my_metadata_t);

  if (metadata->size == full_page_payload_size) {
    // #Return Page STEP 2 : if that Merged block's size is 4096 - sizeof(my_metadata_t), return to system by calling munmap_to_system
    munmap_to_system(metadata, 4096);
  }else {
    // If it's not a full page, add it to its proper size bin
    my_add_to_free_list(metadata);
  }
  
}

// This is called at the end of each challenge.
void my_finalize(){
  printf("Well done Fuka!");
}

void test() {
  // Implement here!
  assert(1 == 1); /* 1 is 1. That's always true! (You can remove this.) */
}
