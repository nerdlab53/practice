import math

class FibonacciNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
        self.degree = 0
        self.mark = False

class FibonacciHeap:
    def __init__(self):
        self.min_node = None
        self.total_nodes = 0

    def insert(self, key, value):
        new_node = FibonacciNode(key, value)
        if not self.min_node:
            self.min_node = new_node
        else:
            self._add_to_root_list(new_node)
            if new_node.key < self.min_node.key:
                self.min_node = new_node
        self.total_nodes += 1
        return new_node

    def extract_min(self):
        if not self.min_node:
            return None
        min_node = self.min_node
        if min_node.child:
            child = min_node.child
            while True:
                next_child = child.right
                self._add_to_root_list(child)
                child.parent = None
                if child == min_node.child:
                    break
                child = next_child
        self._remove_from_root_list(min_node)
        if min_node == min_node.right:
            self.min_node = None
        else:
            self.min_node = min_node.right
            self._consolidate()
        self.total_nodes -= 1
        return min_node

    def decrease_key(self, node, new_key):
        if new_key > node.key:
            raise ValueError("New key is greater than current key")
        node.key = new_key
        parent = node.parent
        if parent and node.key < parent.key:
            self._cut(node, parent)
            self._cascading_cut(parent)
        if self.min_node is None or node.key < self.min_node.key:
            self.min_node = node

    def _add_to_root_list(self, node):
        if not self.min_node:
            self.min_node = node
        else:
            node.right = self.min_node.right
            node.left = self.min_node
            self.min_node.right.left = node
            self.min_node.right = node

    def _remove_from_root_list(self, node):
        node.left.right = node.right
        node.right.left = node.left

    def _consolidate(self):
        max_degree = int(math.log2(self.total_nodes)) + 1
        degree_table = [None] * max_degree
        current = self.min_node
        root_list = []
        while current not in root_list:
            root_list.append(current)
            current = current.right
        for root in root_list:
            degree = root.degree
            while degree_table[degree]:
                other = degree_table[degree]
                if root.key > other.key:
                    root, other = other, root
                self._link(other, root)
                degree_table[degree] = None
                degree += 1
            degree_table[degree] = root
        self.min_node = None
        for root in degree_table:
            if root:
                if not self.min_node:
                    self.min_node = root
                else:
                    self._add_to_root_list(root)
                    if root.key < self.min_node.key:
                        self.min_node = root

    def _link(self, child, parent):
        self._remove_from_root_list(child)
        child.parent = parent
        if not parent.child:
            parent.child = child
            child.left = child
            child.right = child
        else:
            child.left = parent.child
            child.right = parent.child.right
            parent.child.right.left = child
            parent.child.right = child
        parent.degree += 1
        child.mark = False

    def _cut(self, child, parent):
        parent.degree -= 1
        if parent.child == child:
            parent.child = child.right
        if parent.degree == 0:
            parent.child = None
        self._remove_from_root_list(child)
        self._add_to_root_list(child)
        child.parent = None
        child.mark = False

    def _cascading_cut(self, node):
        parent = node.parent
        if parent:
            if not node.mark:
                node.mark = True
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)
