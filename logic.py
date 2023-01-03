from structures.linked_list import LinkedList


class Logic:
    def __init__(self, linkedlist: LinkedList):
        self.linkedList = linkedlist
        self.steps = []
        self.killed = []

    def survivor(self) -> list:
        return self.steps[-1]

    def josephus(self, k: int, index: int) -> list:
        self.steps.append(self.linkedList.get_values())

        if len(self.linkedList) == 1:
            return self.steps

        index = ((index + k) % len(self.linkedList))

        if index == 0:  # if the current node is head
            self.killed.append(self.linkedList.node_at(index))
            self.linkedList.remove_head()
        elif index == len(self.linkedList) - 1:  # if the current node is tail
            self.killed.append(self.linkedList.node_at(index))
            self.linkedList.remove_tail()
        else:  # if the current node is in the middle
            self.killed.append(self.linkedList.node_at(index))
            self.linkedList.remove_at(index)

        self.josephus(k, index)

        return self.steps

    def get_steps(self) -> list:
        return self.steps

    def get_killed(self) -> list:
        return self.killed
