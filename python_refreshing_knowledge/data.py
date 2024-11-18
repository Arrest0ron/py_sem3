class Stack:
    def __init__(self, x=None):
        self.data = []          # Initialize an empty list
        if x is not None:
            self.data.append(x) # Only add `x` if it’s not None
    
    def pop(self):
        if not self.data:       # Check if the stack is empty
            return None
        return self.data.pop()  # Remove and return the last element

    def push(self, x):
        self.data.append(x)      # Append the new element

    @property
    def size(self):
        return len(self.data) 
    

class BinarySearchTree:
    def __init__(self, x=None):
        self.top = TreeNode(x) if x is not None else None

    def insert(self, x):
        if self.top is None:
            self.top = TreeNode(x)
        else:
            self._insert_recursive(x, self.top)

    def _insert_recursive(self, x, currentNode):
        # Check if currentNode's data is None, handle appropriately
        if currentNode.data is None:
            currentNode.data = x
            return

        if x > currentNode.data:
            if currentNode.rchild is None:
                currentNode.rchild = TreeNode(x)
            else:
                self._insert_recursive(x, currentNode.rchild)
        else:
            if currentNode.lchild is None:
                currentNode.lchild = TreeNode(x)
            else:
                self._insert_recursive(x, currentNode.lchild)

        

        
class TreeNode:
    lchild, rchild, data  = None, None, None
    def __init__(self, x = None):
        self.data = x
        if (x):
            self.lchild = TreeNode()
            self.rchild = TreeNode()    
def main():
    a = BinarySearchTree()
    a.insert(5)
    
    a.insert(2)
    a.insert(7)
    
    a.insert(1)
    a.insert(3)
    
    a.insert(6)
    a.insert(8)
    
    return 0    

main()