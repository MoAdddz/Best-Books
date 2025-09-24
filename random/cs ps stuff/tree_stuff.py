import heapq

class Node:
    def __init__(self, symbol=None, freq=0, left=None, right=None):
        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Node(symbol={self.symbol}, freq={self.freq})"
# leaves
a = Node('a', 3)
b = Node('b', 2)

heap = []
heapq.heappush(heap, (a.freq, a))
heapq.heappush(heap, (b.freq, b))

# combine into a parent
parent = Node(None, a.freq + b.freq, a, b)

print("Parent:", parent)
print(" Left:", parent.left)
print(" Right:", parent.right)

f1, n1 = heapq.heappop(heap)
print(f1)
print(n1)

item = heapq.heappop(heap)
print("Popped item:", item)
print(item[1].symbol)