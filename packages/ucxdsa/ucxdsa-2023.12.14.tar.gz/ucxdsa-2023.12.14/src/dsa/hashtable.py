class HashTable:
    def __init__(self, capacity=20):
        self.capacity = capacity

        self.array = []
        for _ in range(self.capacity):
            self.array.append([])
        self.count = 0
        
    def hash_function(self, key):
        charsum = sum(ord(c) * i for i, c in enumerate(key, 1))
        return charsum % self.capacity      
        
    def key_exists(self, key):
        ''' returns a Boolean on whether a key exists in the hashtable or not '''
        bucket = self.hash_function(key)
        if self.array[bucket] is None:
            return False
        
        for e in self.array[bucket]:
            if e[0] == key:
                return True
        return False

    def set(self, key, value):
        ''' if key exists, replace the value 
            otherwise, create a new key-pair
        '''

        bucket = self.hash_function(key)

        # linear searh for key 
        for e in self.array[bucket]:
            if e[0] == key:
                e[1] = value
                break
        else:
            self.array[bucket].append([ key, value ])
            self.count += 1

    def get(self, key):
        ''' get corresponding value of key
            return None if key is not found
        '''
        bucket = self.hash_function(key)

        for e in self.array[bucket]:
            if e[0] == key:
                return e[1]

        return None

    def delete(self, key):
        ''' delete key-value pair if specified key is found '''
        bucket = self.hash_function(key)

        for i in range(len(self.array[bucket])):
            kvpair = self.array[bucket][i]
            if kvpair and kvpair[0] == key:
                del self.array[bucket][i]
                self.count -= 1
                break
    
    def __repr__(self):
        s = ""
        for i, bucket in enumerate(self.array):
            s += f"Bucket {i}: {bucket}\n"
        return s

