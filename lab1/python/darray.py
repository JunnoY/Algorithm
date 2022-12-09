from enum import Enum
from math import floor
import config
import sys


class darray:
    def __init__(self):
        self.array = []
        self.sorted = False
        self.mode = config.mode
        self.verbose = config.verbose

    def insert(self, string):
        self.array.append(string)

        # changing the self.array means it may no longer be sorted
        self.sorted = False

    def find(self, value):
        if (config.mode == SearchModes.LINEAR_SEARCH.value):
            # TODO implement linear search through list
            #  (linear search)
            for i in self.array:
                if value == i:
                    return True
            else:
                return False
        else:
            if (not self.sorted):
                if (self.verbose > 0):
                    print("Dynamic self.array not sorted, sorting... \n")

                self.sort(self.mode)
                if (self.verbose > 0):
                    print("Dynamic self.array sorted\n")

                self.sorted = True

            # TODO implement binary search through self.array
            # search value in array (binary search)
            lower_bound = 0
            upper_bound = len(self.array) - 1
            while lower_bound <= upper_bound:
                middle = floor((lower_bound + upper_bound) / 2)
                if (self.array[middle] < value):
                    lower_bound = middle + 1
                elif (self.array[middle] > value):
                    upper_bound = middle - 1
                else:
                    return True
        return False

    def print_set(self):
        print("Dself.array:\n")
        for i in range(len(self.array)):
            print("\t%s\n" % self.array[i])

    def print_stats(self):
        print("Dynamic self.array contains %d elements\n" % len(self.array))

    def sort(self, select):
        if (select == SearchModes.BINARY_SEARCH_ONE.value):
            self.insertion_sort()
        elif (select == SearchModes.BINARY_SEARCH_TWO.value):
            self.quick_sort()
        elif (select == SearchModes.BINARY_SEARCH_THREE.value):
            print("Nothing Implemented\n")
        elif (select == SearchModes.BINARY_SEARCH_FOUR.value):
            print("Nothing Implemented\n")
        elif (select == SearchModes.BINARY_SEARCH_FIVE.value):
            print("Nothing Implemented\n")
        #  Add your own choices here
        else:
            sys.stderr.write("The value %d is not supported\n" % select)
            sys.exit(23)

    # You may find this helpful
    # It swaps the element at index a and the element at index b in self.array
    def swap(self, a, b):
        temp = self.array[a]
        self.array[a] = self.array[b]
        self.array[b] = temp

    def insertion_sort(self):
        for i in range(1, len(self.array)):
            key = self.array[i]
            for j in range(i - 1, -1, -1):
                if self.array[j] > key:
                    self.array[j + 1] = self.array[j]
                    self.array[j] = key

    # Hint: you probably want to define a help function for the recursive call
    def partition(self, low, high):
        pivot = self.array[low]
        i = low
        j = high
        while (i < j):
            while i <= high and self.array[i] <= pivot:
                i += 1
            while j >= low and self.array[j] > pivot:
                j -= 1
            if (i < j):
                temp = self.array[i]
                self.array[i] = self.array[j]
                self.array[j] = temp
        temp = self.array[low]
        self.array[low] = self.array[j]
        self.array[j] = temp
        return j

    def quicksort(self, low, high):
        if low < high:
            pi = self.partition(self.array, low, high)
            self.quicksort(self.array, low, pi - 1)
            self.quicksort(self.array, pi + 1, high)

    def quick_sort(self):
       self.quicksort(0, len(self.array) - 1)


class SearchModes(Enum):
    LINEAR_SEARCH = 0
    BINARY_SEARCH_ONE = 1
    BINARY_SEARCH_TWO = 2
    BINARY_SEARCH_THREE = 3
    BINARY_SEARCH_FOUR = 4
    BINARY_SEARCH_FIVE = 5
