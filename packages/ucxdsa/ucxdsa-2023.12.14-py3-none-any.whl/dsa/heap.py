class Heap:
    def __init__(self):
        self.array = []
    
    def root(self):
        if self.count() == 0:
            return None

        return self.array[0]
    
    def last(self):
        if self.count() == 0:
            return None

        return self.array[-1] 
    
    def left_index(self, index):
        return (index * 2) + 1

    def right_index(self, index):
        return (index * 2) + 2

    def parent_index(self, index):
        return (index - 1) // 2
    
    def has_left(self, index):
        return self.left_index(index) < self.count()
    
    def has_right(self, index):
        return self.right_index(index) < self.count()

    def has_parent(self, index):
        return self.parent_index(index) >= 0
    
    def insert(self, value):
        self.array.append(value)
        
        start_index = self.count() - 1
        self.heapify_up(start_index)
    
    def heapify_up(self, index):
        parent_index = self.parent_index(index)
        while self.has_parent(index) and self.array[index] > self.array[parent_index]:
            self.array[index], self.array[parent_index] = self.array[parent_index], self.array[index]
            index = parent_index
            parent_index = self.parent_index(index)

    def pop(self):
        root_value = self.root()
        
        # start at root node
        start_index = 0
        if self.count() == 1:
            self.array.pop()
        else:
            self.array[start_index] = self.array.pop()
        
        self.heapify_down(start_index)
        return root_value
        
    def heapify_down(self, index):
        while self.has_left(index):
            higher_index = self.left_index(index)

            right_index = self.right_index(index)
            if self.has_right(index) and self.array[right_index] > self.array[higher_index]:
                higher_index = right_index
            
            if self.array[index] > self.array[higher_index]:
                break
            else:
                self.array[index], self.array[higher_index] = self.array[higher_index], self.array[index]
                
            index = higher_index
    
    def count(self):
        return len(self.array)
    
    def is_empty(self):
        return self.count() == 0

    def print(self):
        node_count = 1
        for i in range(self.count()):
            if i + 1 >= node_count:
                print()
                node_count *= 2
            print(self.array[i], end=" ")
