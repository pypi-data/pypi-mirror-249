import heapq

class Node:
    def __init__(self, left, right, value=None):
        self.child = [left, right]
        self.value = value
    
    def __lt__(self, other):
        return False
    
    def __repr__(self):
        if self.value is None:
            return "none"
        else:
            return self.value

def character_frequency(s):
    ''' takes a string a returns a dictionary on character frequency '''
    d = {}
    for c in s:
        if c not in d:
            d[c] = 1
        else:
            d[c] += 1
    return d

def build_frequency_table(s):
    ''' accepts a string to encode and returns a heap of the characters '''
    frequency_dictionary = character_frequency(s)
    
    # add to priority queue
    h = []
    for item in frequency_dictionary.items():
        heapq.heappush(h, (item[1], Node(None, None, item[0])))

    return h

def build_huffman_tree(heap):
    ''' accepts a heap and returns a Huffman Tree '''
    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        node = Node(n1[1], n2[1])
        heapq.heappush(heap, (n1[0] + n2[0], node))
    return heap[0][1]

def build_huffman_dictionary(node, bit_string=""):
    ''' given a Huffman Node, build a Huffman Dictionary '''
    d = {}
    if node.child[0] is None and node.child[1] is None:
        return {node.value: bit_string}

    d.update(build_huffman_dictionary(node.child[0], bit_string + '0'))
    d.update(build_huffman_dictionary(node.child[1], bit_string + '1'))

    return d

def huffman_encode(string, hd):
    s = ""
    for c in string:
        s += hd[c]
    return s

def huffman_decode(encoded_data, tree):
    root = tree
    s = ""
    for bit in encoded_data:
        tree = tree.child[int(bit)]
        if tree.child[0] is None and tree.child[1] is None: 
            s += tree.value
            tree = root
    return s

def bitstring_to_bytes(s):
    return bytes(int(s[i : i + 8], 2) for i in range(0, len(s), 8))

def bytes_to_bitstring(ba, bitlength=8):
    s = ""
    for b in ba[:-1]:
        byte = f"{b:08b}"
        s += byte
    
    byte = f"{ba[-1]:b}".zfill(bitlength) 
    s += byte

    return s


