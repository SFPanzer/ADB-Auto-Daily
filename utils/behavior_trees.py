from typing import Callable, List


class IBehaviorNode(object):
    def __init__(self):
        self.parent = None

    def exec(self):
        pass


class SequenceNode(IBehaviorNode):
    def __init__(self):
        super(SequenceNode, self).__init__()
        self.children: List[IBehaviorNode] = []

    def exec(self):
        for child in self.children:
            if not child.exec():
                return False
        else:
            return True


class SelectorNode(IBehaviorNode):
    def __init__(self):
        super(SelectorNode, self).__init__()
        self.children: List[IBehaviorNode] = []

    def exec(self):
        for child in self.children:
            if child.exec():
                return True
        else:
            return False


class ConditionNode(IBehaviorNode):
    def __init__(self, blackboard: dict, condition: Callable[[], bool]):
        super(ConditionNode, self).__init__()
        self.blackboard: dict = blackboard
        self.condition: Callable = condition
        self.child: IBehaviorNode | None = None

    def exec(self):
        if self.condition():
            return self.child.exec()
        else:
            return False


class ActionNode(IBehaviorNode):
    def __init__(self, blackboard: dict, action: Callable[[], bool]):
        super(ActionNode, self).__init__()
        self.blackboard: dict = blackboard
        self.action: Callable = action

    def exec(self):
        return self.action()


class BehaviorTree(object):
    def __init__(self):
        self.root: IBehaviorNode = SequenceNode()
        self.blackboard: dict = {}

    def exec(self):
        self.root.exec()
