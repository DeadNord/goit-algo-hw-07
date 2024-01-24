from tabulate import tabulate
import matplotlib.pyplot as plt
from queue import SimpleQueue


class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

    def __str__(self, level=0, prefix="Root: "):
        ret = "    " * level + prefix + str(self.key) + "\n"
        if self.left:
            ret += self.left.__str__(level + 1, "L--- ")
        if self.right:
            ret += self.right.__str__(level + 1, "R--- ")
        return ret


def display_tree(root, ax=None, horizontal_space=1):
    if not ax:
        fig, ax = plt.subplots(figsize=(12, 8))

    if not root:
        return

    def plot_tree(node, x, y, dx, dy):
        if node:
            ax.scatter(x, y, s=250, color="blue", zorder=2)
            ax.text(
                x,
                y,
                str(node.key),
                color="white",
                ha="center",
                va="center",
                fontweight="bold",
                zorder=3,
            )

            if node.left:
                next_x = x - dx
                next_y = y - dy
                ax.plot([x, next_x], [y, next_y], color="black", linewidth=2, zorder=1)
                plot_tree(node.left, next_x, next_y, dx / 2, dy)

            if node.right:
                next_x = x + dx
                next_y = y - dy
                ax.plot([x, next_x], [y, next_y], color="black", linewidth=2, zorder=1)
                plot_tree(node.right, next_x, next_y, dx / 2, dy)

    plot_tree(root, 0, 0, horizontal_space, 1)

    plt.show()


def get_height(node):
    if not node:
        return 0
    return node.height


def get_balance(node):
    if not node:
        return 0
    return get_height(node.left) - get_height(node.right)


def left_rotate(z):
    y = z.right
    T2 = y.left

    y.left = z
    z.right = T2

    z.height = 1 + max(get_height(z.left), get_height(z.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))

    return y


def right_rotate(y):
    x = y.left
    T3 = x.right

    x.right = y
    y.left = T3

    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))

    return x


def max_value_node(node):
    current = node
    while current.right is not None:
        current = current.right
    return current.key


def min_value_node(node):
    current = node
    while current.left is not None:
        current = current.left
    return current.key


def get_sum_of_values(node):
    if not node:
        return 0
    return node.key + get_sum_of_values(node.left) + get_sum_of_values(node.right)


def insert(root, key):
    if not root:
        return AVLNode(key)

    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    else:
        return root

    root.height = 1 + max(get_height(root.left), get_height(root.right))

    balance = get_balance(root)

    if balance > 1:
        if key < root.left.key:
            return right_rotate(root)
        else:
            root.left = left_rotate(root.left)
            return right_rotate(root)

    if balance < -1:
        if key > root.right.key:
            return left_rotate(root)
        else:
            root.right = right_rotate(root.right)
            return left_rotate(root)

    return root


def delete_node(root, key):
    if not root:
        return root

    if key < root.key:
        root.left = delete_node(root.left, key)
    elif key > root.key:
        root.right = delete_node(root.right, key)
    else:
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left

        temp = min_value_node(root.right)
        root.key = temp
        root.right = delete_node(root.right, temp)

    if root is None:
        return root

    root.height = 1 + max(get_height(root.left), get_height(root.right))

    balance = get_balance(root)

    if balance > 1:
        if get_balance(root.left) >= 0:
            return right_rotate(root)
        else:
            root.left = left_rotate(root.left)
            return right_rotate(root)

    if balance < -1:
        if get_balance(root.right) <= 0:
            return left_rotate(root)
        else:
            root.right = right_rotate(root.right)
            return left_rotate(root)

    return root


def get_tree_structure(root):
    if not root:
        return "Tree is empty"
    return str(root)


def main():
    root = None
    keys = [10, 20, 30, 25, 28, 27, -1]

    operation_data = []
    tree_structure_data = []

    for key in keys:
        root = insert(root, key)
        operation_data.append(("Inserted", key))
        tree_structure_data.append(("After Insertion", get_tree_structure(root)))

    keys_to_delete = [10, 27]

    for key in keys_to_delete:
        root = delete_node(root, key)
        operation_data.append(("Deleted", key))
        tree_structure_data.append(("After Deletion", get_tree_structure(root)))

    max_value = max_value_node(root)
    min_value = min_value_node(root)
    sum_values = get_sum_of_values(root)

    data_table = [
        ("Maximum Value in AVL Tree:", max_value),
        ("Minimal Value in AVL Tree:", min_value),
        ("Sum of All Values in AVL Tree:", sum_values),
    ]

    print("Operation Data:")
    print(tabulate(operation_data, headers=["Operation", "Key"], tablefmt="pipe"))

    print("\nData Table:")
    print(tabulate(data_table, headers=["Operation", "Value"], tablefmt="pipe"))

    print("\nTree Structure Data:")
    print(
        tabulate(
            tree_structure_data,
            headers=["Operation", "Tree Structure"],
            tablefmt="pipe",
        )
    )

    display_tree(root)


if __name__ == "__main__":
    main()
