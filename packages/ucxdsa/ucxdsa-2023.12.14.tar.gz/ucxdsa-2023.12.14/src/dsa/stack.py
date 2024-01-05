class Stack:
    def __init__(self, capacity=10):
        self.array = [None] * capacity
        self.count = 0
    
    def push(self, element):
        if len(self) >= len(self.array):
            raise Exception("Capacity Reached")
        self.count += 1
        self.array[self.top()] = element
        
    def pop(self):
        if self.is_empty():
            raise Exception("Empty Stack")
        element = self.array[self.top()]
        self.count -= 1
        return element
    
    def peek(self):
        if self.is_empty():
            raise Exception("Empty Stack")
        return self.array[self.top()]
    
    def __len__(self):
        return self.count
    
    def is_empty(self):
        return self.count == 0
    
    def top(self):
        return self.count - 1

    def capacity(self):
        return len(self.array)

    def __repr__(self):
        return f"{self.array[0:self.count]} Top: {self.top()} Capacity: {self.capacity()}"
    
    
class DynamicStack(Stack):
    def grow(self):
        # create new array with new size
        new_array = [ None ] * len(self.array) * 2
        
        # copy elements
        for i, e in enumerate(self.array):
            new_array[i] = e

        self.array = new_array

    def shrink(self):
        # create new array with new size
        if self.capacity() < 10:
            return

        new_capacity = self.capacity() // 2
        new_array = [ None ] * new_capacity
        
        # copy elements
        for i in range(new_capacity):
            new_array[i] = self.array[i]

        self.array = new_array


    def check_capacity(self):
        if self.count >= self.capacity():
            self.grow()
        elif self.count * 4 <= self.capacity():
            self.shrink()
        
    def push(self, element):
        self.check_capacity()
        super().push(element)
        
    def pop(self):
        self.check_capacity()
        return super().pop()

