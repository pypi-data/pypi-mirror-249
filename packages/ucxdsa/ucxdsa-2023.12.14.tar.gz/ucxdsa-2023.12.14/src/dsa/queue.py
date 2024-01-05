class Queue:
    def __init__(self, capacity=10):
        self.array = [None] * capacity
        self.front = 0
        self.count = 0
    
    def enqueue(self, element):
        if self.count >= len(self.array):
            raise Exception("Capacity Reached")

        index = (self.front + self.count) % len(self.array)
        self.array[index] = element
        self.count += 1
        
    def dequeue(self):
        if self.is_empty():
            raise Exception("Empty Queue")

        element = self.array[self.front]
        self.front += 1
        if self.front >= len(self.array):
            self.front = 0
        self.count -= 1
        return element
    
    def peek(self):
        if self.is_empty():
            raise Exception("Empty Queue")

        return self.array[self.front]

    def is_empty(self):
        return self.count == 0
    
    def capacity(self):
        return len(self.array)

    def __repr__(self):
        arr = []
        for i in range(self.count):
            index = (i + self.front) % len(self.array)
            arr.append(str(self.array[index]))
        arrstr = ", ".join(arr)
        return f"[{arrstr}] Front: {self.front} count: {self.count} Capacity: {self.capacity()}"
    

# shrink not implemented
class DynamicQueue(Queue):
    def __init__(self, capacity=10):
        self.array = [None] * capacity
        self.front = 0
        self.count = 0
    
    def grow(self):
        # create new array with new size
        new_array = [ None ] * len(self.array) * 2
        
        # copy elements
        for i in range(self.count):
            new_array[i] = self.array[i + self.front]
        self.front = 0
        self.array = new_array

    def check_capacity(self):
        if self.front + self.count >= len(self.array):
            self.grow()

    def enqueue(self, element):
        self.check_capacity()
        index = self.front + self.count
        self.array[index] = element
        self.count += 1

