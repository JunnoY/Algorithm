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
        if (self.mode == SearchModes.LINEAR_SEARCH.value):
            # TODO implement linear search through list
            #  (linear search)
            for i in self.array:
                if value == i:
                    print("Value is found")
            else:
                print("Value is not found")
            print("Linear search not yet implemented")
        else:
            if (not self.sorted):
                if (self.verbose > 0):
                    print("Dynamic self.array not sorted, sorting... \n")

                self.sort(self.mode)
                if (self.verbose > 0):
                    print("Dynamic self.array sorted\n")

                self.sorted = True

            # TODO implement binary search through self.array
            # sort the self.array first (make insertion sort and quick sort)
            # insertion sort
            def insertion_sort(array):
                for i in range(1, len(array)):
                    key = array[i]
                    for j in range(i - 1, -1, -1):
                        if array[j] > key:
                            array[j + 1] = array[j]
                            array[j] = key

            # insertion_sort(self.array)

            # quicksort
            def partition(array, low, high):
                pivot = array[low]
                i = low
                j = high
                while (i < j):
                    while i <= high and array[i] <= pivot:
                        i += 1
                    while j >= low and array[j] > pivot:
                        j -= 1
                    if (i < j):
                        temp = array[i]
                        array[i] = array[j]
                        array[j] = temp
                temp = array[low]
                array[low] = array[j]
                array[j] = temp
                return j

            def quicksort(array, low, high):
                if low < high:
                    pi = partition(array, low, high)
                    quicksort(array, low, pi - 1)
                    quicksort(array, pi + 1, high)
                return array

            # print(quicksort(self.array, 0, len(self.array) - 1))

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
                    print("Value is found")
            else:
                print("Value is not found")
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
        sys.stderr.write("Not implemented\n")
        sys.exit(-1)

    # Hint: you probably want to define a help function for the recursive call
    def quick_sort(self):
        sys.stderr.write("Not implemented\n")
        sys.exit(-1)


class SearchModes(Enum):
    LINEAR_SEARCH = 0
    BINARY_SEARCH_ONE = 1
    BINARY_SEARCH_TWO = 2
    BINARY_SEARCH_THREE = 3
    BINARY_SEARCH_FOUR = 4
    BINARY_SEARCH_FIVE = 5
