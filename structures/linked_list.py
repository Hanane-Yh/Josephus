from structures.node import Node


class LinkedList:

    def __init__(self, values=None):
        self.head = None
        self.tail = None
        if values is not None:
            self.add_multiple_nodes(values)

    def __str__(self) -> str:
        nodes = []
        if self.head is None:
            return "Empty List"
        else:
            current = self.head
            while current.next != self.head:
                nodes.append(current)
                current = current.next
            nodes.append(current)
        return ' -> '.join([str(node) for node in nodes])

    def __len__(self) -> int:
        """returns the length of the list"""
        count = 0
        node = self.head
        while not(node.next == self.head):
            count += 1
            node = node.next
        count += 1
        return count

    def __iter__(self):
        """makes linkedlist iterable"""
        current = self.head
        while current:
            yield current
            current = current.next

    def get_values(self) -> list:
        """returns the values of the list"""
        values = []
        current = self.head
        while current.next != self.head:
            values.append(current.value)
            current = current.next
        values.append(current.value)

        return values

    def add_node(self, value: str) -> Node:
        """adds a single node to the list"""
        # empty list
        if self.head is None:
            self.head = self.tail = Node(value)

        # add the new node to the end of the list
        else:
            self.tail.next = Node(value)
            self.tail = self.tail.next

        self.tail.next = self.head
        return self.tail

    def add_multiple_nodes(self, values: list) -> None:
        """adds multiple nodes to the list"""
        for value in values:
            self.add_node(value)

    def add_as_head(self, value: str) -> None:
        """adds given node as the head of the list"""
        # empty list
        if self.head is None:
            self.head = self.tail = Node(value)

        else:
            self.head = Node(value, next_node=self.head)

    def node_at(self, index: int) -> Node:
        """returns the node at the given index"""
        if index != 0 and index != len(self):
            current = self.head
            i = 0
            while i < index:
                current = current.next
                i += 1
            return current
        elif index == 0:
            return self.head
        elif index == len(self):
            return self.tail

    def remove_head(self) -> None:
        """removes the head of the list"""
        self.head = self.head.next
        self.tail.next = self.head

    def remove_tail(self) -> None:
        """removes the tail of the list"""
        current = self.head
        while not (current.next == self.tail):
            current = current.next
        current.next = self.head
        self.tail = current

    def delete_node(self, node: Node) -> None:
        """removes the given node from the list"""
        current = self.head
        while not (current.next == node):
            current = current.next
        current.next = current.next.next

    def remove_by(self, value: str) -> None:
        """removes the first node with the given value"""
        current = self.head
        while not (current.next.value == value):
            current = current.next
        current.next = current.next.next

    def remove_at(self, index: int) -> None:
        """removes node at the given index from the list"""
        current = self.head

        i = 0
        while i < index - 1:
            current = current.next
            i += 1
        current.next = current.next.next
