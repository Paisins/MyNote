from typing import List


class Node:
    def __init__(self, value: int):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None  # 方便执行删除操作
        self.direction = None

    def __str__(self):
        return str(self.value)

    def __len__(self):
        return len(str(self.value))


class BasicTree:
    """基础树类"""

    Node = Node

    def __init__(self, value: int = None):
        """初始化"""
        if value is not None:
            self.root = self.Node(value)
        else:
            self.root = None

    def get_tree_nodes_on_levels(self, nodes_list: List[list]):
        """
        传入某层的结点, 将下层结点添加进去;
        nodes_list: 每个元素是个list, 包含当前层的所有结点
        """
        next_level_nodes = list()
        for node in nodes_list[-1]:
            if node is None:
                next_level_nodes += [None, None]
            else:
                next_level_nodes += [node.left, node.right]
        if any(next_level_nodes):
            nodes_list.append(next_level_nodes)
            self.get_tree_nodes_on_levels(nodes_list)

    def __str__(self, none_char: str = '*', split_char: str = ' ', split_len: int = 5):
        """
        二叉树可视化
        none_char:  结点为空的默认展示字符
        split_char: 结点之间的分隔符
        split_len:  相邻叶子结点之间的间隔长度, 只能设置奇数, 如果设置为偶数在效果上会自动减一
        """
        nodes_list = [[self.root]]
        self.get_tree_nodes_on_levels(nodes_list)

        depth = len(nodes_list)  # 整颗树的深度
        level_axis_map, node_axis_map = dict(), dict()
        for level_index, nodes in enumerate(nodes_list):
            level_axis_map[level_index] = list()
            for index, node in enumerate(nodes):
                axis_index = self.get_axis_index(depth - level_index, index)
                node_axis_map[axis_index] = node
                level_axis_map[level_index].append(axis_index)

        tree_str = list()
        for level_index, axis_nodes in level_axis_map.items():
            level_str = ''
            for index in range(1, axis_nodes[-1] + 1):
                node = node_axis_map[index]
                if index in axis_nodes:
                    level_str += str(node) if node else none_char
                else:
                    level_str += len(node) * split_char if node else len(none_char) * split_char
                level_str += (split_len - 1) // 2 * split_char
            tree_str.append(level_str + '\n')

        str_tree = "\n".join(tree_str)
        return str_tree

    def get_axis_index(self, height: int, index: int):
        """
        获取每个结点在数轴上的位置, 从1开始
        height: 结点在树中的高度, 叶子结点层的高度为1
        index: 结点在该层的位置, 从0开始
        """
        return 2 ** (height - 1) + index * 2 ** (height)


class BinaryTree(BasicTree):
    """二叉树"""

    def add_node(self, value: int):
        """新增结点"""
        node = self.Node(value)
        if not self.root:
            self.root = node
            return node

        nodes = [self.root]
        while nodes:
            next_nodes = list()
            for n in nodes:
                if n.left is None:
                    direction = 'left'
                    break
                elif n.right is None:
                    direction = 'right'
                    break
                next_nodes += [n.left, n.right]
            else:
                nodes = next_nodes
                continue
            node.parent = n
            node.direction = direction
            setattr(n, direction, node)
            break
        return node

    def get_node(self, value: int):
        """根据值查找结点"""
        if self.root is None:
            return None

        nodes = [self.root]
        for n in nodes:
            if n is None:
                continue
            elif n.value == value:
                return n
            else:
                nodes += [n.left, n.right]

    def delete_node(self, node: Node):
        """删除结点"""
        if not node:
            return

        parent = node.parent
        if node.left is None:
            setattr(parent, node.direction, node.left)
        elif node.right is None:
            setattr(parent, node.direction, node.right)
        else:
            next_node = node
            while next_node.left or next_node.right:
                if next_node.left:
                    next_node = next_node.left
                elif next_node.right:
                    next_node = next_node.right

            node.value = next_node.value
            setattr(next_node.parent, next_node.direction, None)


if __name__ == '__main__':
    # data = list(range(0, 10))
    data = [0, 10, 19, 2, 1, 13, 4, 17, 18, 6, 123]

    tree = BinaryTree()
    for i in data:
        tree.add_node(i)
    print('添加结果')
    print(tree)

    node = tree.get_node(13)
    print('获取node', node)
    tree.delete_node(node)
    print('删除后结果')
    print(tree)

    node = tree.get_node(0)
    print('获取node', node)
    tree.delete_node(node)
    print('删除后结果')
    print(tree)
