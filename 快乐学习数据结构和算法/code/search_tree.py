from binary_tree import BinaryTree


class SearchTree(BinaryTree):
    """遍历树"""
    def pre_order_search_v1(self, node, value):
        # 默认二叉树中值是唯一的
        if not node:
            return None
        if node.value == value:
            return node
        left_result = self.pre_order_search_v1(node.left, value)
        if left_result:
            return left_result
        right_result = self.pre_order_search_v1(node.right, value)
        if right_result:
            return right_result
        return None

    def in_order_search_v1(self, node, value):
        # 默认二叉树中值是唯一的
        if not node:
            return None
        left_result = self.in_order_search_v1(node.left, value)
        if left_result:
            return left_result
        print(node.value)
        if node.value == value:
            return node
        right_result = self.in_order_search_v1(node.right, value)
        if right_result:
            return right_result
        return None

    def post_order_search_v1(self, node, value):
        # 默认二叉树中值是唯一的
        if not node:
            return None
        left_result = self.post_order_search_v1(node.left, value)
        if left_result:
            return left_result
        right_result = self.post_order_search_v1(node.right, value)
        if right_result:
            return right_result
        print(node.value)
        if node.value == value:
            return node
        return None

    def level_search_v1(self, node_list, value):
        # 默认二叉树中值是唯一的
        new_node_list = list()
        for node in node_list:
            print(node.value)
            if node.value == value:
                return node
            if node.left:
                new_node_list.append(node.left)
            if node.right:
                new_node_list.append(node.right)
        if new_node_list:
            return self.level_search_v1(new_node_list, value)
        else:
            return None

    @staticmethod
    def pre_order_search_v2(node, value):
        # 默认二叉树中值是唯一的
        if not node:
            return None
        node_list = [node]
        while node_list:
            node = node_list.pop()
            if node is None:
                continue
            print(node.value)
            if node.value == value:
                return node
            node_list.append(node.right)
            node_list.append(node.left)
        return None

    @staticmethod
    def in_order_search_v2(node, value):
        # 默认二叉树中值是唯一的
        if not node:
            return None

        node_list = list()
        while True:
            print([i.value for i in node_list], node.value if node else None)
            if node:
                node_list.append(node)
                node = node.left
            elif node_list:
                node = node_list.pop()
                print(node.value)
                if node.value == value:
                    return node
                node = node.right
            else:
                break
        return None

    @staticmethod
    def post_order_search_v2(node, value):
        # 默认二叉树中值是唯一的
        pass

    @staticmethod
    def level_search_v2(node, value):
        # 默认二叉树中值是唯一的
        node_list = [node]
        while node_list:
            node = node_list.pop(0)
            print(node)
            if node.value == value:
                return node
            if node.left:
                node_list.append(node.left)
            if node.right:
                node_list.append(node.right)
        else:
            return None

    def level_print(self, node_list):
        next_node_list = list()
        for node in node_list[-1]:
            if node is None:
                next_node_list += [None, None]
            else:
                next_node_list += [node.left, node.right]
        if any(next_node_list):
            node_list.append(next_node_list)
            self.level_print(node_list)
        else:
            return node_list


if __name__ == '__main__':
    # data = [5, 4, 8, 3, 4.5]
    data = [5.0, 4.0, 8.0, 3.0, 4.5, 9.0, 2.0, 4.2, 4.7]
    tree = SearchTree()
    for i in data:
        tree.add(i)
    print("添加结果：")
    print(tree)

    # 测试遍历-递归
    # tree.pre_order_search_v1(tree.root, 1000)
    # print('---------------------')
    # tree.in_order_search_v1(tree.root, 1000)
    # print('---------------------')
    # tree.post_order_search_v1(tree.root, 1000)
    # print('---------------------')
    # tree.level_search_v1([tree.root], 1000)
    # print('---------------------')
    # 测试遍历-迭代
    # tree.pre_order_search_v2(tree.root, 1000)
    # print('---------------------')
    # tree.in_order_search_v2(tree.root, 1000)
    # print('---------------------')
    # tree.post_order_search_v2(tree.root, 1000)
    # print('---------------------')
    # tree.level_search_v2(tree.root, 1000)
    # print('---------------------')

    # tree.add(4.1)
    # print(tree)