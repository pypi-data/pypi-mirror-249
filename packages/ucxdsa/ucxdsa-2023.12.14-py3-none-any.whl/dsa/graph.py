class AdjacencyMatrixGraph:
    ''' adjacency matrix graph (unweighted, directed and undirected)'''
    def __init__(self, labels):
        ''' accepts a list of vertices labels '''
        self.labels = labels
        self.label_index = { label: index for index, label  in enumerate(labels) }

        node_count = len(self.labels)
        self.array = [[None for i in range(node_count)] for j in range(node_count)]

    def add_edge(self, a_label, b_label):
        self.add_adjacent_vertex(a_label, b_label)
        
    def add_adjacent_vertex(self, a_label, b_label):
        a = self.label_index[a_label]
        b = self.label_index[b_label]
        self.array[a][b] = True
        self.array[a][a] = True

        self.array[b][a] = True
        self.array[b][b] = True

    def add_directed_edge(self, a_label, b_label):
        self.add_adjacent_directed_vertex(a_label, b_label)

    def add_directed_adjacent_vertex(self, a_label, b_label):
        self.add_adjacent_directed_vertex(a_label, b_label)
        
    def add_adjacent_directed_vertex(self, a_label, b_label):
        a = self.label_index[a_label]
        b = self.label_index[b_label]
        self.array[a][b] = True
        self.array[a][a] = True
        self.array[b][b] = True

    def df_traverse(self, start_label):
        return self.df_rec_traverse(start_label, dict())
        
    def df_rec_traverse(self, start_label, visited):
        start_index = self.label_index[start_label]
        visited[start_index] = True
        print(self.labels[start_index])
        
        for i in range(len(self.array)):
            if i not in visited and self.array[start_index][i]:
                self.df_rec_traverse(self.labels[i], visited)

    def bf_traverse(self, start_label):
        q = []
        visited={}
        start_index = self.label_index[start_label]
        q.append(start_index)

        while len(q) > 0:
            current = q.pop(0) # equivalent of dequeue

            if current not in visited: 
                visited[current] = True
                print(self.labels[current])

                for i in range(len(self.array)):
                    if self.array[current][i]:
                        q.append(i)

    def print_graph(self):
        print("   |", end="")
        for label in self.labels:
            print(f"{label:^3}", end=" ")
        print()
        print("----" * (len(self.array) + 1))
        for r, row in enumerate(self.array):
            label = self.labels[r]
            print(f"{label:^3}|", end="");
            for col in row:
                b = " T " if col else "   "
                print(b, end=" ")
            print()
            
class AdjacencyMatrixWeightedGraph:
    ''' adjacency matrix graph (weighted, directed and undirected)'''
    def __init__(self, labels):
        ''' accepts a list of vertices labels '''
        self.labels = labels
        self.label_index = { label: index for index, label  in enumerate(labels) }

        node_count = len(self.labels)
        self.array = [[None for i in range(node_count)] for j in range(node_count)]

    def add_edge(self, a_label, b_label, weight):
        self.add_adjacent_vertex(a_label, b_label, weight)

    def add_adjacent_vertex(self, a_label, b_label, weight):
        a = self.label_index[a_label]
        b = self.label_index[b_label]

        self.array[a][b] = weight
        self.array[a][a] = 0

        self.array[b][a] = weight
        self.array[b][b] = 0

    def add_directed_edge(self, a_label, b_label, weight):
        self.add_adjacent_directed_vertex(a_label, b_label, weight)

    def add_directed_adjacent_vertex(self, a_label, b_label, weight):
        self.add_adjacent_directed_vertex(a_label, b_label, weight)

    def add_adjacent_directed_vertex(self, a_label, b_label, weight):
        a = self.label_index[a_label]
        b = self.label_index[b_label]

        self.array[a][b] = weight
        self.array[a][a] = 0
        self.array[b][b] = 0
        
    def print_graph(self):
        print("   |", end="")
        for label in self.labels:
            print(f"{label:>3}", end=" ")
        print()
        print("----" * (len(self.array) + 1))
        for r, row in enumerate(self.array):
            label = self.labels[r]
            print(f"{label:^3}|", end="");
            for col in row:
                w = f"{col:3}" if col is not None else "   "
                print(w, end=" ")
            print()
            
            
class Vertex:
    ''' adjacency list vertex - unweighted directed and undirected '''
    def __init__(self, value):
        self.value = value
        self.adjacents = []
        
    def add_adjacent_vertex(self, vertex):
        if vertex not in self.adjacents:
            self.adjacents.append(vertex)
        if self not in vertex.adjacents:
            vertex.add_adjacent_vertex(self)
        
    def add_edge(self, vertex):
        self.add_adjacent_vertex(vertex)

    def add_directed_edge(self, vertex):
        self.add_directed_adjacent_vertex(vertex)
        
    def add_directed_adjacent_vertex(self, vertex):
        if vertex not in self.adjacents:
            self.adjacents.append(vertex)

    def df_traverse(self):
        self.df_traverse_rec(self, dict())

    def df_traverse_rec(self, vertex, visited={}):
        visited[vertex] = True
        print(vertex.value)
        
        for v in vertex.adjacents:
            if not visited.get(v, False):
                v.df_traverse_rec(v, visited)
            
    def bf_traverse(self):
        start = self
        visited = {}
        queue = []
        
        queue.append(start)

        while len(queue) > 0:
            current = queue[0]
            del queue[0]
            
            if not visited.get(current, False):               
                visited[current] = True
                print(current.value)
        
                for v in current.adjacents:
                    queue.append(v)
        
    def dfs(self, end):
        return self.dfs_rec(self, end, dict())
        
    def dfs_rec(self, current, end, visited=None):
        if current.value == end.value:
            print("Found: ", end.value)
            return current

        visited[current] = True
        print(current.value)
        
        for v in current.adjacents:
            if not visited.get(v, False):
                return v.dfs_rec(v, end, visited)
        return None
    
    def bfs(self, end):
        visited = {}
        queue = []
        start = self
        
        visited[start] = True
        queue.append(start)

        while len(queue) > 0:
            current = queue[0]
            del queue[0]
            print(current.value)
            # print("Visited: ", visited)
            # print("Queue: ", queue)
            
            if current.value == end.value:
                return current
            
            for v in current.adjacents:
                if not visited.get(v, False):               
                    visited[v] = True
                    queue.append(v)
        
        return None

    def __repr__(self):
        return self.value

class WeightedVertex:
    ''' adjacency list vertex - weighted directed and undirected '''
    def __init__(self, value):
        self.value = value
        self.adjacents = {}
        
    # same as add_adjacent_vertex
    def add_edge(self, vertex, weight):
        self.add_adjacent_vertex(vertex, weight)

    # same as add_directed_adjacent_vertex
    def add_directed_edge(self, vertex, weight):
        self.add_directed_adjacent_vertex(vertex, weight)

    def add_directed_adjacent_vertex(self, vertex, weight):
        if vertex not in self.adjacents:
            self.adjacents[vertex] = weight

    def add_adjacent_vertex(self, vertex, weight):
        if vertex not in self.adjacents:
            self.adjacents[vertex] = weight
        if self not in vertex.adjacents:
            vertex.adjacents[self] = weight
        
    def df_traverse(self, vertex, visited={}):
        visited[vertex] = True
        print(vertex.value)
        
        for v in vertex.adjacents:
            if not visited.get(v, False):
                v.df_traverse(v, visited)
            
    def bf_traverse(self, vertex):
        visited = {}
        queue = []
        
        queue.append(vertex)

        while len(queue) > 0:
            current = queue[0]
            del queue[0]
            
            if not visited.get(current, False):               
                visited[current] = True
                print(current.value)
        
                for v in current.adjacents:
                    queue.append(v)
                    
    def dfs(self, end):
        return self.dfs_rec(self, end, dict())
        
    def dfs_rec(self, current, end, visited={}):
        print(current.value, visited.keys())
        if current.value == end.value:
            return current

        visited[current] = True
        print("Current: ", current.value)
        
        for v in current.adjacents:
            if not visited.get(v, False):
                v.dfs_rec(v, end, visited)
        return None

    
    def bfs(self, vertex, value):
        visited = {}
        queue = []
        
        queue.append(vertex)

        while len(queue) > 0:
            current = queue[0]
            del queue[0]
            
            if current.value == value:
                return current
            
            if not visited.get(current, False):               
                visited[current] = True
                print(current.value)
        
                for v in current.adjacents:
                    queue.append(v)
        return None
    
    def __repr__(self):
        return self.value

    def __lt__(self, vertex):
        return self.value < vertex.value

    
#### Dijkstra's Algorithm Functions

def shortest_path(start, end):
    weight_table = {}
    previous = {}
    visited = {}
    queue = [] # ideally, a min heap
    
    current = start
    queue.append(current)
    weight_table[current.value] = 0
    previous[current.value] = current
    
    while len(queue) > 0:
        current_weight = weight_table.get(current.value, None)
        visited[current.value] = True

# for non-weighted version, use:
# for adjacent in current.adjacents:
#   weight = 1

        for adjacent, weight in current.adjacents.items():
            if not visited.get(adjacent.value, False):
                queue.append(adjacent)

            wt = weight_table.get(adjacent.value, None)
            if not wt or wt > weight + current_weight:
                print(weight_table)
                weight_table[adjacent.value] = weight + current_weight
                previous[adjacent.value] = current

        current = queue[0]
        del queue[0]
            
    return weight_table, previous

def find_path(start, end):
    weight_table, previous = shortest_path(start, end)
    path = []

    current = end
    path.append(current.value)
    while current != start:
        current = previous[current.value]
        path.append(current.value)
        
    path.reverse()
    print("weight table")
    print(weight_table)
    print("price ", weight_table[end.value])
    return path

