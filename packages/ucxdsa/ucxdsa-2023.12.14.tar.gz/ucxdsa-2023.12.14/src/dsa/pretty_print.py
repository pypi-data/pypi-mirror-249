import math

def heap_print(heap):
    ''' print a heap '''
    if len(heap) == 0:
        return
    height = math.floor(math.log2(len(heap)))
    level_str = ""
    current_level = 0
    value_width = 3
    max_width = 2 ** (height - 1) * value_width

    for index, node in enumerate(heap):
        level = int(math.log2(index + 1))
        columns = 2 ** (level - 1)
        column_width = int(max_width / columns)
        if current_level != level:
            current_level = level
            print(level_str)
            level_str = ""
        level_str += f"{node:^{column_width}}"
    print(level_str)
    print()


def tree_to_array(node, index=0, tree_array=None):
    ''' create an array filled with index and value pairs from a node based tree '''
    if not tree_array:
        tree_array = []
    if node is None:
        return
    tree_array.append((index, node.value))
    tree_to_array(node.left, index * 2 + 1, tree_array)
    tree_to_array(node.right, index * 2 + 2, tree_array)
    
    return tree_array

def get_tree_height(node):
    ''' calculate the height of a binary tree '''
    if node is None:
        return 0
    else:
        return max(get_tree_height(node.left) + 1, get_tree_height(node.right) + 1)

def fill_complete_tree(tree):
    ''' make a binary tree a complete tree '''
    tree_array = tree_to_array(tree.root)
    tree_height = get_tree_height(tree.root)

    # build empty complete tree
    array_size = (2 ** tree_height) - 1
    new_tree = [ "" ] * array_size

    # fill the complete tree array
    for index, value in tree_array:
        new_tree[index] = value
    return new_tree

def tree_print(tree):
    ''' pretty print a binary tree '''
    complete_tree = fill_complete_tree(tree)
    heap_print(complete_tree)
