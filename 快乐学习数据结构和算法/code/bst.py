from binary_tree import BasicTree, Node


class BSTTree(BasicTree):
    """二叉搜索树"""

    def add(self, value: int):
        """新增结点"""
        if not self.root:
            self.root = self.Node(value)
            return self.root

        node = self.Node(value)
        next_node = self.root
        while True:
            if value < next_node.value:
                child_node = next_node.left
                direction = 'left'
            elif value > next_node.value:
                child_node = next_node.right
                direction = 'right'
            else:  # 不允许重复结点
                return next_node
            if child_node:
                next_node = child_node
            else:
                node.parent = next_node
                node.direction = direction
                setattr(next_node, direction, node)
                break
        return node

    def get_node(self, value: int):
        """根据值查找结点"""
        if not self.root:
            return

        next_node = self.root
        while next_node:
            if next_node.value == value:
                return next_node
            elif value < next_node.value:
                next_node = next_node.left
            else:
                next_node = next_node.right

    def delete_value(self, value):
        """删除输入值对应的结点"""
        node = self.get_node(value)
        if node:
            node = self.delete(node)
        return node

    def delete(self, node: Node):
        """删除结点"""
        # assert node is not None, 'delete node should not be None'

        while True:
            if node.left is not None:
                delete_node = self.get_max(node.left)
                node.value, delete_node.value = delete_node.value, node.value
            elif node.right is not None:
                delete_node = self.get_min(node.right)
                node.value, delete_node.value = delete_node.value, node.value
            else:
                setattr(node.parent, node.direction, None)
                return node
            node = delete_node

    def get_min(self, node: Node):
        """获取小于结点的最小值"""
        while node.left:
            node = node.left
        return node

    def get_max(self, node: Node):
        """获取大于结点的最大值"""
        while node.right:
            node = node.right
        return node


if __name__ == '__main__':
    data = [10, 5, 20, 0, 7, 15, 25, 12, 17, 22, 30]
    # data = list(range(5))
    # data = [5, 4, 6, 2, 8, 1, 3, 7, 9, 4.5]
    tree = BSTTree()
    for i in data:
        tree.add(i)
    print("添加结果：")
    print(tree)
    # 测试一
    value = 12
    tree.delete_value(value)
    print(f"删除{value}结果: ")
    print(tree)
    value = 17
    tree.delete_value(value)
    print(f"删除{value}结果: ")
    print(tree)
    # 测试二
    value = 20
    tree.delete_value(value)
    print(f"删除{value}结果: ")
    print(tree)
    # 测试三
    value = 6
    tree.add(6)
    print(f"添加{value}结果：")
    print(tree)
    value = 10
    tree.delete_value(value)
    print(f"删除{value}结果: ")
    print(tree)
