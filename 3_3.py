# coding=utf-8
# Дана простая реализация бинарного дерева в виде класса Tree. В классе
# реализован метод добавления элементов к дереву. Задача – реализовать
# еще два метода:
# - метод find(value). В качестве аргумента метод принимает
# значение (число). Метод должен возвращать True, если элемент
# найден в дереве или False, если такой элемент отсутствует.
# - метод print(). Этот метод не принимает никаких аргументов.
# Результат работы метода – вывод структуры дерева (значений его
# элементов и иерархии) на экран (вывод может иметь любой
# осмысленный вид, но запрещается выводить все элементы в одну
# строку).

class Tree:
    def __init__(self, value, root=None):
        # left and right child nodes
        self.lchild = None
        self.rchild = None
        # node value
        self.value = value
        # parent element for current node
        self.root = root

    def __contains__(self, item):
        return self.find(item)

    def add(self, value):
        # track current node (level)
        current_node = self
        # track parent node
        last_node = None
        # search the place to insert new node
        while current_node:
            last_node = current_node
            if value > current_node.value:
                current_node = current_node.rchild
            elif value < current_node.value:
                current_node = current_node.lchild
            else:
                # element already presented in tree
                return False
        # create new node and link it with parent
        new_node = Tree(value, last_node)
        if value > last_node.value:
            last_node.rchild = new_node
        else:
            last_node.lchild = new_node
            return True

    def find(self, value):
        def _findByNode(node, val):
            if node is None:
                return False
            elif val == node.value:
                return True
            elif val < node.value:
                return _findByNode(node.lchild, val)
            else:
                return _findByNode(node.rchild, val)

        return _findByNode(self, value)

    def print(self):
        def _height(node):
            if node is None:
                return 0
            else:
                left = _height(node.lchild)
                right = _height(node.rchild)
                if left > right:
                    return left + 1
                else:
                    return right + 1

        def _printLevel(node, level, interval):
            if node is None and level == 1:
                print("(  )".center(interval), end="")
                return

            if level == 1:
                print(("(%d)" % node.value).center(interval), end="")
                return
            else:
                _printLevel(node if node is None else node.lchild, level - 1, interval)
                _printLevel(node if node is None else node.rchild, level - 1, interval)

        for i in range(1, _height(self) + 1):
            step = 2 ** (_height(self) - i) * 4
            _printLevel(self, i, step)
            print("")

# Test
root = Tree(10)
root.add(9)
root.add(8)
root.add(11)
root.add(15)
root.add(16)
root.add(12)
root.add(2)
root.add(3)
root.add(14)
root.add(65)

print(root.find(11))

print(root.find(5))

if 1 in root:
    print(True)
else:
    print(False)

root.print()
