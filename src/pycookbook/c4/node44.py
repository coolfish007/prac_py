class Node:
    def __init__(self, value):
        super().__init__()
        self.value = value
        self._children = []

    def __repr__(self):
        return f"Node({self.value})"

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        print(f"before yield:{self}")
        yield self
        print(f"after yield:{self}")
        for n in self:
            print(f"in for {n}")
            # 加一层循环,驱动depth_first的调用.
            for s in n.depth_first():
                print(s)

    def depth_first_yield_from(self):
        """ yield from, 会把控制权传递给调用者.
        for 中起到委派生成器的作用.
         """
        print(f"inner print:before yield:{self}")
        yield self
        print(f"inner print:after yield:{self}")
        for n in self:
            yield from n.depth_first_yield_from()

    def width_first(self, isRoot):
        if isRoot:
            yield self

        i = 1
        for n in self:
            yield n
            if len(self._children) == i:
                # 重新从节点1开始遍历
                for s in self:
                    yield from s.width_first(False)
            else:
                i += 1
