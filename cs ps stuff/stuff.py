import math
from collections import Counter
import heapq

text = "hello huffman"

symbols = []
for symbol in text:
    if symbol not in symbols:
        symbols.append(symbol)
print(symbols)

freqs = Counter(text) #freqs is a dictionary with characters as keys and their frequencies as values

total = sum(freqs.values())

probs=[]
for f in freqs.values():
    if f > 0:
        probs.append(f / total)

def measure_entropy(probs):
    entropy = 0
    for p in probs:
        if p > 0:
            entropy += p * math.log2(p)
    entropy = -entropy
    return entropy
entropy = measure_entropy(probs)

print("Entropy:", entropy)

class Node:
    def __init__(self, freq=0, symbol=None, left=None, right=None):
        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right

    def __repr__(self): # like a 2nd name
        return f"Node(freq={self.freq}, symbol={self.symbol})"
    
    def __lt__(self, other):
        return self.freq < other.freq
    
# Create a heap with (frequency, symbol) pairs
# This is a min-heap, so the smallest frequency will be at the root
heap = []
nodes = []
for symbol in freqs:
    node=Node(freq=freqs[symbol],symbol=symbol)
    heapq.heappush(heap, (node.freq,node))
    nodes.append(node)
print("Heap:", heap)
print("Nodes: ", nodes)


while len(heap)>1:
    f1, n1 = heapq.heappop(heap)

    f2, n2 = heapq.heappop(heap)

    parent = Node(f1+f2, None, n1, n2)
    nodes.append(parent)
    heapq.heappush(heap,(parent.freq,parent))
print(f"Nodes : {nodes}")
print(heap)
root = heapq.heappop(heap)[1]