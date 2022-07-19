from binary_tree import BasicTree, Node


class HuffmanTree(BasicTree):
    """哈夫曼树"""

    def __init__(self, values: list):
        self.root = None

        v_nodes = dict()
        while values:
            if self.root is not None:
                values.append(self.root.value)
            # todo 每次进来都排序？不能执行插入操作吗？
            values = sorted(values, reverse=True)

            v1 = values.pop()
            v2 = values.pop()
            self.root = Node(v1 + v2)
            node_1 = self._get_node(v1, v_nodes)
            node_2 = self._get_node(v2, v_nodes)
            self.root.left = node_1
            self.root.right = node_2

            if self.root.value not in v_nodes:
                v_nodes[self.root.value] = list()
            v_nodes[self.root.value].append(self.root)

    @staticmethod
    def _get_node(value: int, v_nodes: list):
        """根据值从v_nodes中获取node"""
        if value in v_nodes:
            node = v_nodes[value].pop()
            if not v_nodes[value]:
                del v_nodes[value]
        else:
            node = Node(value)
        return node


if __name__ == '__main__':
    values = [2, 3, 6, 8, 9]
    tree = HuffmanTree(values)
    print(tree)
