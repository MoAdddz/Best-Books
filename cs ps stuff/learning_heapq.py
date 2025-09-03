import heapq

# start with an empty list
heap = []

# push (priority, value) pairs
heapq.heappush(heap, (5, 'a'))
heapq.heappush(heap, (2, 'b'))
heapq.heappush(heap, (7, 'c'))

print("Heap list:", heap)  # notice it keeps the smallest at index 0
# pop smallest
#smallest = heapq.heappop(heap)
#print("Popped:", smallest)

#print("Heap now:", heap)