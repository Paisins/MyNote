from enum import Enum
from python_bst import BSTTree


class SpinType(str, Enum):
    """旋转类型"""
    left = 'left'
    right = 'right'


class Node:
    def __init__(self, value: int, color: str):
        self.color = color
        self.value = value
        self.left = None
        self.right = None
        self.parent = None  # 方便执行删除操作
        self.direction = None

    def __str__(self):
        if self.color == 'r':
            return f'\033[31m{self.value}\033[0m'
        else:
            return f'\033[38m{self.value}\033[0m'

    def __len__(self):
        return len(str(self.value))


class BRTree(BSTTree):
    """红黑树"""

    def __init__(self, value: int = None):
        """初始化"""
        if value is not None:
            self.root = Node(value=value, color='b')
        else:
            self.root = None

    def _get_uncle(self, node: Node):
        """获取叔叔结点"""
        if node is None:
            return None
        elif node.parent is None:
            return None
        elif node.parent.parent is None:
            return None

        if node.parent.direction == 'right':
            uncle_node = node.parent.parent.left
        else:
            uncle_node = node.parent.parent.right
        return uncle_node

    def _get_brother(self, node: Node):
        """获取兄弟结点"""
        if node is None:
            return
        elif node.parent is None:
            return None

        if node.direction == 'right':
            brother_node = node.parent.left
        else:
            brother_node = node.parent.right

        return brother_node

    def _add(self, value: int):
        """新增结点"""
        if not self.root:
            self.root = Node(value, color='b')
            return self.root

        node = self.root
        while node is not None:
            node_father = node
            if node.value >= value:
                node = node.left
            else:
                node = node.right

        node = Node(value=value, color='r')
        node.parent = node_father
        if node_father.value <= value:
            node_father.right = node
            node.direction = 'right'
        else:
            node_father.left = node
            node.direction = 'left'
        return node

    def add_node(self, value: int):
        """添加结点"""

        node = self._add(value)
        # debug
        # if node.value == 9:
        #     print("debug parent: ", node, node.parent, node.direction)
        self.keep_add_balance(node)

        # node = self.get_node(7)
        # if node:
        #     print(f"debug 2: left and right [{node}]", node.left, node.right)

    def delete_node(self, value: int):
        """删除结点"""
        node = self.get_node(value=value)
        print("get node: ", node, node.left, node.right)
        deleted_node = self.delete(node)  # 获取真正被删除的结点
        # print("deleted_node", deleted_node)
        # print("before balance", self)
        self.keep_delete_balance(deleted_node)

    def keep_add_balance(self, node: Node):
        """添加后保持平衡"""

        if node.parent is None:           # 情况一：当前结点是根结点
            node.color = 'b'
        elif node.parent.color == 'b':    # 情况二：当前结点的父结点为黑色
            pass
        elif node.parent.color == 'r':    # 情况二：当前结点的父结点为红色
            uncle_node = self._get_uncle(node)
            if uncle_node is None or uncle_node.color == 'b':
                # 这里跟平衡二叉树的旋转基本一致
                if node.direction == 'left' and node.parent.direction == 'left':
                    node.parent.color, node.parent.parent.color = 'b', 'r'
                    self.spin(node=node.parent, spin_type=SpinType.right.value)
                elif node.direction == 'right' and node.parent.direction == 'right':
                    node.parent.color, node.parent.parent.color = 'b', 'r'
                    self.spin(node=node.parent, spin_type=SpinType.left.value)
                elif node.direction == 'right' and node.parent.direction == 'left':
                    node.color, node.parent.parent.color = 'b', 'r'
                    self.spin(node=node, spin_type=SpinType.left.value)
                    self.spin(node=node, spin_type=SpinType.right.value)
                elif node.direction == 'left' and node.parent.direction == 'right':
                    node.color, node.parent.parent.color = 'b', 'r'
                    self.spin(node=node, spin_type=SpinType.right.value)
                    self.spin(node=node, spin_type=SpinType.left.value)
            else:
                uncle_node.color = 'b'
                node.parent.color = 'b'
                node.parent.parent.color = 'r'
                self.keep_add_balance(node=node.parent.parent)
        # todo 判断一下添加结点14之后，结点9的父结点情况
        # if node == 14

    def keep_delete_balance(self, deleted_node: Node):
        """删除后保持平衡"""
        # fixme 这里如果是删除根结点还是会报错
        # 情况一：被删除结点是红色，对平衡无影响
        if deleted_node.color == 'r':
            return
        parent_node = deleted_node.parent
        brother_node = self._get_brother(node=deleted_node)
        # fixme 如果兄弟结点为空呢？
        # 情况二：被删除结点是黑色，兄弟结点是红色
        if brother_node.color == 'r':
            brother_node.color, parent_node.color = 'b', 'r'
            if brother_node.direction == 'right':
                self.spin(node=brother_node, spin_type=SpinType.left.value)
            else:
                self.spin(node=brother_node, spin_type=SpinType.right.value)
        # 情况三：被删除结点兄弟结点的右结点是红色
        elif brother_node.direction == 'right' and brother_node.right.color == 'r':
            brother_node.right.color = 'b'
            # 兄弟结点和父结点的颜色互换
            brother_node.color, parent_node.color = parent_node.color, brother_node.color
            self.spin(node=brother_node, spin_type=SpinType.left.value)
        elif brother_node.direction == 'left' and brother_node.left.color == 'r':
            brother_node.left.color = 'b'
            # 兄弟结点和父结点的颜色互换
            brother_node.color, parent_node.color = parent_node.color, brother_node.color
            self.spin(node=brother_node, spin_type=SpinType.right.value)
        # 情况四：被删除结点兄弟结点的左结点是红色
        elif brother_node.direction == 'right' and brother_node.left.color == 'r':
            brother_node.color, brother_node.left.color = 'r', 'b'
            self.spin(node=brother_node.left, spin_type=SpinType.right.value)

            # 这里兄弟结点变了
            brother_node = parent_node.right
            brother_node.right.color = 'b'
            brother_node.color, parent_node.color = parent_node.color, brother_node.color
            self.spin(node=brother_node, spin_type=SpinType.left.value)
        elif brother_node.direction == 'left' and brother_node.right.color == 'r':
            brother_node.color, brother_node.right.color = 'r', 'b'
            self.spin(node=brother_node.right, spin_type=SpinType.left.value)

            # 这里兄弟结点变了
            brother_node = parent_node.left
            brother_node.left.color = 'b'
            brother_node.color, parent_node.color = parent_node.color, brother_node.color
            self.spin(node=brother_node, spin_type=SpinType.right.value)
        # 情况五：被删除结点兄弟结点的无红色子结点
        else:
            brother_node.color = 'r'
            self.keep_add_balance(node=parent_node)

    def spin(self, node: Node, spin_type: SpinType):
        """
        旋转算法
        node: 平衡结点, 旋转过程中心的结点
        """
        parent_node = node.parent

        if spin_type == SpinType.right.value:
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
        elif spin_type == SpinType.left.value:
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
    data = [16, 3, 7, 11, 9, 26, 18, 14, 15]
    print('example', data)
    tree = BRTree()
    for i in data:
        tree.add_node(i)
    print(tree)
    # print(f"debug 1: after add node[{i}]\n", tree)
    # 删除根结点返回的结果不对
    # 1. 9的父结点是11，方向是左
    # 2. add 9之后就是如此
    # 3. 添加9的时候7结点的左右分别是3,16
    # 4. 9的父结点一直都是11，在添加了14旋转之后没有修改
    tree.delete_node(11)
    print(tree)
