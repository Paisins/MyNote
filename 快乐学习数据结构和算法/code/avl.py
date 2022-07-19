from bst import BSTTree


class Node:
    def __init__(self, value: int):
        self.value = value
        self.bf = 0   # 左子树的深度减去右子树的深度
        self.left = None  # 其实应该改成 lchild 和 rchild
        self.right = None
        self.parent = None  # 方便执行删除操作
        self.direction = None

    def __str__(self):
        # return f'{self.value}({self.bf})'  # 打印bf值
        return f'{self.value}'

    def __len__(self):
        return len(str(self))


class AVLTree(BSTTree):
    """平衡二叉树"""

    Node = Node

    def add(self, value: int):
        """添加结点"""
        if not self.root:
            self.root = self.Node(value)
            return self.root

        node = super().add(value)
        self.check_bf(node, 'add')
        return node

    def delete(self, node: Node):
        """删除结点"""
        if not node:
            return
        delete_node = super().delete(node)
        self.check_bf(delete_node, 'delete')

    def check_bf(self, node: Node, change_type: str):
        """
        node: 新增结点或者被删结点
        change_type: add / delete / no_change
        从新添加或者被删除的结点开始往上更正bf值, 以及检查每个父结点是否平衡
        """
        parent = node.parent
        if not parent:
            return

        if change_type == 'add':
            if node.direction == 'left':
                parent.bf += 1
            else:
                parent.bf -= 1
            if parent.bf in (0, 2, -2):
                change_type = 'no_change'
        elif change_type == 'delete':
            if node.direction == 'left':
                parent.bf -= 1
            else:
                parent.bf += 1
            if parent.bf in (-1, 1):
                change_type = 'no_change'
        else:
            return
        if parent.bf in (-2, 2):
            # 平衡之后，父结点发生了变化
            parent = self.balance_spin(parent)
        self.check_bf(parent, change_type)

    def balance_spin(self, node: Node):
        """
        node: 不平衡的结点
        平衡算法，判断旋转方式，返回平衡后的父结点
        """
        # 右边子树高
        if node.bf == -2:
            if node.right.bf == -1:
                # 调整bf值
                spin_node = node.right
                node.bf = spin_node.bf = 0
                self.spin(node=node.right, spin_type='left')
            else:
                # 调整bf值
                spin_node = node.right.left
                if spin_node.bf == 0:
                    node.bf = node.right.bf = 0
                elif spin_node.bf == -1:
                    node.bf = 1
                    node.right.bf = 0
                elif spin_node.bf == 1:
                    node.bf = 0
                    node.right.bf = -1
                self.spin(node=spin_node, spin_type='right')
                self.spin(node=spin_node, spin_type='left')
        # 左边子树高
        else:
            if node.left.bf == 1:
                # 调整bf值
                spin_node = node.left
                node.bf = node.left.bf = 0
                self.spin(node=node.left, spin_type='right')

            else:
                # 调整bf值
                spin_node = node.left.right
                if spin_node.bf == 0:
                    node.bf = node.left.bf = 0
                elif spin_node.bf == -1:
                    node.bf = 0
                    node.left.bf = 1
                elif spin_node.bf == 1:
                    node.bf = -1
                    node.left.bf = 0
                self.spin(node=spin_node, spin_type='left')
                self.spin(node=spin_node, spin_type='right')
        return spin_node

    def spin(self, node: Node, spin_type: str):
        """旋转算法"""
        parent_node = node.parent

        if spin_type == 'right':
            parent_node.left = node.right
            node.right = parent_node

            if parent_node.parent is None:
                self.root = node
                node.parent = None
            else:
                node.parent = parent_node.parent
                node.direction = parent_node.direction
                setattr(parent_node.parent, parent_node.direction, node)
            parent_node.parent = node
            parent_node.direction = 'right'
        elif spin_type == 'left':
            parent_node.right = node.left
            node.left = parent_node

            if parent_node.parent is None:
                self.root = node
                node.parent = None
            else:
                node.parent = parent_node.parent
                node.direction = parent_node.direction
                setattr(parent_node.parent, parent_node.direction, node)
            parent_node.parent = node
            parent_node.direction = 'left'


if __name__ == '__main__':
    # data = [5, 4, 8, 3, 4.5]
    data = [5.0, 4.0, 8.0, 3.0, 4.5, 9.0, 2.0, 4.2, 4.7]
    tree = AVLTree()
    for i in data:
        tree.add(i)
    print("添加结果：")
    print(tree)

    # 测试 ll
    tree.add(1)
    print("测试ll, 添加1: ")
    print(tree)
    # 测试 rr
    tree.add(10)
    print("测试rr, 添加10: ")
    print(tree)
    # 测试lr
    tree.add(7.0)
    print("测试lr-1, 添加7.0: ")
    print(tree)
    tree.add(7.5)
    print("测试lr-2, 添加7.5: ")
    print(tree)
    # 测试rl
    node = tree.add(12)
    print("测试rl-1, 添加12: ")
    print(tree)
    node = tree.add(11)
    print("测试rl-2, 添加11: ")
    print(tree)

    # 测试删除

    node = tree.add(13)
    print("测试删除: rr-1, 添加13: ")
    print(tree)
    tree.delete_value(10)
    print("测试删除: rr-2, 删除10: ")
    print(tree)

    node = tree.add(0.5)
    print("测试删除: ll-1, 添加0.5: ")
    print(tree)
    tree.delete_value(3.0)
    print("测试删除: ll-2, 删除3.0: ")
    print(tree)

    tree.delete_value(0.5)
    tree.delete_value(4.2)
    tree.delete_value(4.5)
    print(tree)
    print("测试删除: lr-1, 删除0.5, 4.2, 4.5: ")
    print(tree)
    tree.delete_value(4.7)
    print("测试删除: lr-2, 删除4.7: ")
    print(tree)

    tree.delete_value(13)
    tree.delete_value(7.0)
    tree.delete_value(8.0)
    print("测试删除: rl-1, 删除13, 7.0, 8.0: ")
    print(tree)
    tree.delete_value(7.5)
    print("测试删除: rl-2, 删除7.5: ")
    print(tree)

    # 测试任意删除
    tree.delete_value(5.0)
    print("测试删除任意结点5.0: ")
    print(tree)
    tree.delete_value(4.0)
    print("测试删除任意结点4.0: ")
    print(tree)
    tree.delete_value(1)
    print("测试删除任意结点1: ")
    print(tree)
