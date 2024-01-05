class Array:
    def __init__(self, contents=None, capacity=10):
        ''' contents are optional list/array to fill the array '''
        self.array = [ None ] * capacity
        self.count = 0

        if contents:
            self.extend(contents)
        
    def append(self, element):
        if self.count >= self.capacity():
            raise Exception(f"Capacity Error: {len(self)} maximum")

        self.array[self.count] = element
        self.count += 1

    def extend(self, array):
        ''' append each element from a given array '''
        for e in array:
            self.append(e)

    def insert(self, index, element):
        ''' insert element at index '''
        if index < 0 or index >= self.count:
            raise IndexError

        self.shift_right(self.count, index)
        self.array[index] = element
        self.count += 1
        
    def shift_right(self, start, end):
        for i in range(start, end, -1):
            self.array[i] = self.array[i - 1]

    def delete(self, index):
        ''' delete element at index '''
        if index >= self.count or index < 0:
            raise IndexError

        self.shift_left(index, self.count)
        self.count -= 1

    def shift_left(self, start, end):
        for i in range(start, end):
            self.array[i] = self.array[i + 1]

    ### special methods for handling index operator
    def __getitem__(self, index):
        if index < 0 or index >= self.count: 
            raise IndexError
        return self.array[index]
            
    def __setitem__(self, index, value):
        if index < 0 or index >= self.count: 
            raise IndexError
        self.array[index] = value
        
    ### special methods for len()
    def __len__(self):
        return self.count

    def capacity(self):
        return len(self.array)

    ### override the representation value with the Python interpreter
    def __repr__(self):
        contents = self.array[:self.count]
        return f'{contents} Count: {self.count} Capacity: {self.capacity()}'

class DynamicArray(Array):
    def grow(self):
        ''' create new array with double capacity '''
        new_size = len(self.array) * 2
        new_array = [ None ] * new_size

        # copy elements
        for i in range(len(self.array)):
            new_array[i] = self.array[i]

        self.array = new_array

    def shrink(self):
        ''' create new array with half capacity '''
        new_size = len(self.array) // 2
        new_array = [ None ] * new_size
        
        # copy elements
        for i in range(new_size):
            new_array[i] = self.array[i]

        self.array = new_array

    def check_capacity(self):
        if self.count >= len(self.array):
            self.grow()
        elif self.count * 4 <= len(self.array):
            self.shrink()

    def append(self, element):
        self.check_capacity()

        self.array[self.count] = element
        self.count += 1

    def extend(self, array):
        ''' append each element from a given array '''
        for e in array:
            self.append(e)

    def insert(self, index, element):
        if index >= self.count or index < 0:
            raise IndexError

        self.check_capacity()

        self.shift_right(self.count, index)
        self.array[index] = element
        self.count += 1
        
    def delete(self, index):
        if index >= self.count or index < 0:
            raise IndexError

        self.check_capacity()

        self.shift_left(index, self.count)
        self.count -= 1

        
