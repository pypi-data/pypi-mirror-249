class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def print(self, level=0):
        ''' print contents of a tree horizontally '''
        if self.right:
            self.right.print(level + 1)
        print("   " * level + str(self.value))
        if self.left:
            self.left.print(level + 1)

class Tree:
    def __init__(self, node=None):
        self.root = node
        
    def search(self, value):
        ''' returns node of value if found, otherwise, return None '''
        current = self.root
        
        while current is not None:
            if value == current.value:
                return current
            elif value < current.value:
                current = current.left
            elif value > current.value:
                current = current.right
            else:
                return None
        
        return None
    
    def insert(self, value):
        current = self.root
        if self.root is None:
            self.root = Node(value)
            return
        
        while current is not None:
            if value < current.value:
                if current.left is None:
                    current.left = Node(value)
                    return
                else:
                    current = current.left
            elif value > current.value:
                if current.right is None:
                    current.right = Node(value)
                    return
                else:
                    current = current.right
            else:
                return 
   
    def delete(self, value):
        ''' delete node with given value '''
        return self.delete_node(value, self.root)
        
    def delete_node(self, value, node):
        if node is None:
            return None
        
        if value < node.value:
            node.left = self.delete_node(value, node.left)
        elif value > node.value:
            node.right = self.delete_node(value, node.right)
        else:
            if node.left is None:
                branch = node.right
                node = None
                return branch
            elif node.right is None:
                branch = node.left
                node = None
                return branch
            
            branch = self.min_node(node.right)
            node.value = branch.value
            node.right = self.delete_node(branch.value, node.right)
            
        return node
    
    def min_node(self, node=None):
        if node is None:
            node = self.root
        
        if node.left is None:
            return node
        else:
            return self.min_node(node.left)
    
    def print(self):
        self.root.print()
        
        
