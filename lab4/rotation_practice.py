"""Parts 3-4: implement AVL balance factor, rotations, and iterative and recursive AVL insertion.

Node structure, tree container, and height maintenance helpers are provided.
"""

class Node:
    """Binary Search Tree node with parent pointer and height attribute."""

    def __init__(self, key, parent=None):
        self.key = key
        self.parent = parent
        self.left = None
        self.right = None
        self.height = 0

    def __repr__(self):
        return 'Node(' + str(self.key) + ')'

class BinarySearchTree:
    """Container holding the root pointer of a Binary Search Tree."""

    def __init__(self):
        self.root = None

    def print_tree(self):
        """Print the full tree with child labels, heights, balance factors, and parents."""
        if self.root is None:
            print('(empty tree)')
            return
        seen = set()

        def node_summary(node):
            left_height = -1 if node.left is None else node.left.height
            right_height = -1 if node.right is None else node.right.height
            bf = left_height - right_height
            parent_key = 'None' if node.parent is None else str(node.parent.key)
            return str(node.key) + ' [height=' + str(node.height) + ', bf=' + str(bf) + ', parent=' + parent_key + ']'

        def print_children(node, prefix):
            if node.left is None and node.right is None:
                return
            children = [('L', node.left), ('R', node.right)]
            for index, (direction, child) in enumerate(children):
                is_last = index == len(children) - 1
                connector = '└── ' if is_last else '├── '
                child_prefix = prefix + ('    ' if is_last else '│   ')
                if child is None:
                    print(prefix + connector + direction + ': None')
                elif id(child) in seen:
                    print(prefix + connector + direction + ': ' + node_summary(child) + ' [cycle or repeated reference]')
                else:
                    seen.add(id(child))
                    print(prefix + connector + direction + ': ' + node_summary(child))
                    print_children(child, child_prefix)
        seen.add(id(self.root))
        print(node_summary(self.root))
        print_children(self.root, '')

def get_height(node):
    """Provided: return height of node (-1 for None, 0 for leaf)."""
    if node is None:
        return -1
    return node.height

def update_height(node):
    """Provided: recalculate node's height based on its left and right children."""
    if node is not None:
        node.height = 1 + max(get_height(node.left), get_height(node.right))

def balance_factor(node):
    """Calculate balance factor: height(node.left) - height(node.right).

  Return 0 if node is None.
  """
    return 0 if node is None else get_height(node.left) - get_height(node.right)

def rotate_left(tree, x):
    """Perform a single left rotation around node x.

  Pivots on x's right child y. Updates child pointers, parent pointers,
  tree.root (if x was root), and recalculates heights for x and y.
  """
    y = x.right
    assert y is not None
    x.right = y.left
    if y.left is not None:
        y.left.parent = x
    y.parent = x.parent
    if x.parent is None:
        tree.root = y
    elif x.parent.left is x:
        x.parent.left = y
    else:
        x.parent.right = y
    y.left = x
    x.parent = y
    update_height(x)
    update_height(y)
    return y

def rotate_right(tree, y):
    """Perform a single right rotation around node y.

  Pivots on y's left child x. Updates child pointers, parent pointers,
  tree.root (if y was root), and recalculates heights for y and x.
  """
    x = y.left
    assert x is not None
    y.left = x.right
    if x.right is not None:
        x.right.parent = y
    x.parent = y.parent
    if y.parent is None:
        tree.root = x
    elif y.parent.left is y:
        y.parent.left = x
    else:
        y.parent.right = x
    x.right = y
    y.parent = x
    update_height(y)
    update_height(x)
    return x

def rotate_left_right(tree, z):
    """Perform a double Left-Right (LR) rotation around node z.

  Rotates left on z's left child, then rotates right on z.
  """
    rotate_left(tree, z.left)
    return rotate_right(tree, z)

def rotate_right_left(tree, z):
    """Perform a double Right-Left (RL) rotation around node z.

  Rotates right on z's right child, then rotates left on z.
  """
    rotate_right(tree, z.right)
    return rotate_left(tree, z)

def avl_insert_iterative(tree, key):
    """Insert a key iteratively, restore AVL balance, and return its Node."""
    parent = None
    current = tree.root
    while current is not None:
        if key == current.key:
            return current
        parent = current
        current = current.left if key < current.key else current.right
    node = Node(key, parent)
    if parent is None:
        tree.root = node
    elif key < parent.key:
        parent.left = node
    else:
        parent.right = node
    current = parent
    while current is not None:
        update_height(current)
        bf = balance_factor(current)
        if bf > 1:
            if balance_factor(current.left) < 0:
                rotate_left(tree, current.left)
            rotate_right(tree, current)
            break
        if bf < -1:
            if balance_factor(current.right) > 0:
                rotate_right(tree, current.right)
            rotate_left(tree, current)
            break
        current = current.parent
    return node

def avl_insert_recursive(tree, key):
    """Insert a key recursively, restore AVL balance, and return its Node."""
    inserted = None

    def insert(root, parent):
        nonlocal inserted
        if root is None:
            inserted = Node(key, parent)
            return inserted
        if key == root.key:
            inserted = root
            return root
        if key < root.key:
            root.left = insert(root.left, root)
        else:
            root.right = insert(root.right, root)
        update_height(root)
        bf = balance_factor(root)
        if bf > 1:
            if balance_factor(root.left) < 0:
                rotate_left(tree, root.left)
            return rotate_right(tree, root)
        if bf < -1:
            if balance_factor(root.right) > 0:
                rotate_right(tree, root.right)
            return rotate_left(tree, root)
        return root
    tree.root = insert(tree.root, None)
    tree.root.parent = None
    return inserted
if __name__ == '__main__':
    from lab_checks import check_rotations
    raise SystemExit(check_rotations(balance_factor, rotate_left, rotate_right, rotate_left_right, rotate_right_left, avl_insert_iterative, avl_insert_recursive))
