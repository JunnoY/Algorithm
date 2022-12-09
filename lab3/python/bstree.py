import config
import time


class bstree:
    def __init__(self):
        self.verbose = config.verbose

    global number_comparison_insert, number_comparison_find, start_time, end_time, total_time, number_find
    number_comparison_insert = 0
    number_comparison_find = 0
    start_time = 0
    end_time = 0
    total_time = 0
    number_find =0

    def size(self):
        if self.tree():
            return 1 + self.left.size() + self.right.size()
        return 0

    def tree(self):
        # This counts as a tree if it has a field self.value
        # it should also have sub-trees self.left and self.right
        return hasattr(self, 'value')

    # This is the insert function, which is used to insert a value into a tree
    # The function first check if the tree that we try to insert value in has a value at its root node:
    # If there is no value at the root node, the value will be inserted to the root node of the tree, then the function
    # initialises the left subtree and the right subtree of the current tree
    # (self.left = bstree() and self.right = bstree())

    # If there is value at the root node of the current tree, we compare the value we try to insert with the value
    # at the root node: if the value we try to insert is less than the value at the root node, we insert the value to
    # the left subtree of the current tree, by self.left.insert(value), this insert function will be called again, but
    # the tree that calling it becomes the left subtree of the current tree;
    # if the value we try to insert is greater than the value at the root node, we insert the value to the right subtree
    # of the current tree, by self.right.insert(value), this insert function will be called again,
    # but the tree that calling it becomes the right subtree of the current tree.

    # This process will repeat recursively, until the value is inserted to the tree.

    def insert(self, value):
        global number_comparison_insert, start_time, end_time, total_time
        start_time = time.time()
        if self.tree():
            # TODO if tree is not NULL then insert into the correct sub-tree
            if value < self.value:
                number_comparison_insert += 1
                self.left.insert(value)
                end_time = time.time()
                total_time += end_time-start_time
                return True
            elif value > self.value:
                number_comparison_insert += 1
                self.right.insert(value)
                end_time = time.time()
                total_time += end_time - start_time
                return True
        else:
            # TODO otherwise create a new node containing the value
            self.value = value
            self.right = bstree()
            self.left = bstree()
            end_time = time.time()
            total_time += end_time - start_time
            return True

    # This is the find function, which is used to insert a value into a tree The function first check if the tree has
    # a value, if not it will return False. Then the function compares the value we try to find with the value at the
    # root node of the tree, if they equal, returns True. Otherwise, if the value we try to find is less than the
    # value at the root of the tree, the right_subtree of the current tree will call the find function, and the same
    # process repeat, but this time we compare the value at the root node of the right subtree (of the original tree)
    # with the value we try to find; else, the left_subtree of the current tree will call the find function instead,
    # and the same process repeat, but this time we compare the value at the root node of the left subtree (of the
    # original tree) with the value we try to find
    # This process will repeat recursively, until the value is found in the tree.
    def find(self, value):
        global number_comparison_find, number_find
        if self.tree():
            # TODO complete the find function
            if self.value is not None:
                if self.value == value:
                    number_comparison_find += 1
                    number_find += 1
                    return True

                elif value < self.value:
                    number_comparison_find += 1
                    if self.left is None:
                        number_find += 1
                        return False
                    return self.left.find(value)

                else:
                    if self.right is None:
                        number_find += 1
                        return False
                    return self.right.find(value)
        return False

    # You can update this if you want
    def print_set_recursive(self, depth):
        if self.tree():
            for i in range(depth):
                print(" ", end='')
            print("%s" % self.value)
            self.left.print_set_recursive(depth + 1)
            self.right.print_set_recursive(depth + 1)

    # You can update this if you want
    def print_set(self):
        print("Tree:\n")
        self.display()

    def get_height(self):
        if self.tree():
            if self.left.tree() and self.right.tree():
                return 1 + max(self.left.get_height(), self.right.get_height())
            elif self.left.tree():
                return 1 + self.left.get_height()
            elif self.right.tree():
                return 1 + self.right.get_height()
            else:
                return 1
        else:
            return 1

    def display(self):
        if self.tree():
            lines, *_ = self.display_part()
            for line in lines:
                print(line)

    def display_part(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.tree():
            if not self.right.tree() and not self.left.tree():
                line = '%s' % self.value
                width = len(line)
                height = 1
                middle = width // 2
                return [line], width, height, middle
            # Only left child.
            if not self.right.tree():
                lines, n, p, x = self.left.display_part()
                s = '%s' % self.value
                u = len(s)
                first_line = (x + 1) * ' ' + (n - x - 1) * ' ' + s
                second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
                shifted_lines = [line + u * '' for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2
            # Only right child.
            if not self.left.tree():
                lines, n, p, x = self.right.display_part()
                s = '%s' % self.value
                u = len(s)
                first_line = s + x * ' ' + (n - x) * ' '
                second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
                shifted_lines = [u * ' ' + line for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2
            # Two children.
            left, n, p, x = self.left.display_part()
            right, m, q, y = self.right.display_part()
            s = '%s' % self.value
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * ' ' + s + y * ' ' + (m - y) * ' '
            second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
            if p < q:
                left += [n * ' '] * (q - p)
            elif q < p:
                right += [m * ' '] * (p - q)
            zipped_lines = zip(left, right)
            lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
            return lines, n + m + u, max(p, q) + 2, n + u // 2
        else:
            print("There is no tree")

    # average find = total number of comparison in find / total number of values we try to find(number of values infile)
    # average insert = total number of comparison in insert / total number of elements inserted
    def print_stats(self):
        global number_comparison_insert, number_comparison_find, total_time, number_find
        # TODO update code to record and print statistic
        height = self.get_height()
        avg_insert = number_comparison_insert / self.size()
        avg_find = number_comparison_find / number_find
        print("Height: " + str(height - 1))
        print("Average comparison per insert: " + str(avg_insert))
        print("Average comparison per find: " + str(avg_find))
        print("Total time for insert: " + str(total_time*1000) + "ms")
        print("Average time per insert: " + str(total_time*1000/self.size()) + "ms")
