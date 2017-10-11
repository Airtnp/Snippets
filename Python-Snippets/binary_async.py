# ref: http://simeonvisser.com/posts/python-3-using-yield-from-in-generators-part-2.html
class Node:
    def __init__(self, value):
        self.left = []
        self.value = value
        self.right = []

    def iterate(self):
        for node in self.left:
            yield node.value
        yield self.value
        for node in self.right:
            yield node.value

    def process(self):
        input_value = yield self.value
    # ...

    def child_iterate(self, nodes):
        for node in nodes:
            yield from node.process()

    def node_iterate(self):
        yield from self.child_iterate(self.left)
        self.process()
        yield from self.child_iterate(self.right)

def main():
    root = Node(0)
    root.left = [Node(i) for i in [1, 2, 3]]
    root.right = [Node(i) for i in [4, 5, 6]]
    for value in root.node_iterate():
        print(value)

if __name__ == "__main__":
    main()