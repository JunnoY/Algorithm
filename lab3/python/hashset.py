from enum import Enum
import config
import time


class hashset:
    def __init__(self):
        # TODO: create initial hash table
        self.copy_table = None  # for rehash use
        self.verbose = config.verbose
        self.mode = config.mode
        self.hash_table_size = config.init_size
        self.hash_table_size_prime = self.nextPrime(self.hash_table_size)
        self.table = [cell() for _ in range(self.hash_table_size_prime)]
        self.collision = 0
        self.num_entries = self.hash_table_size_prime
        self.start = 0
        self.end = 0
        self.total_time = 0
        self.num_rehash = 0

    # Helper functions for finding prime numbers
    def isPrime(self, n):
        i = 2
        while i * i <= n:
            if n % i == 0:
                return False
            i = i + 1
        return True

    def nextPrime(self, n):
        while not self.isPrime(n):
            n = n + 1
        return n

    # An ASCII function which it finds the ASCII value of each character in the input value, and calculates the power of
    # 2 of the ASCII value. It finally returns the value of sum of all powered values % size of the hash table.
    # the value
    # This hash function is quite slow in terms of speed, there might be many collisions occur
    def hash_ascii(self, value):
        hash_value = 0
        for i in range(len(value)):
            hash_value += ord(value[i]) ** 3
        return hash_value % self.hash_table_size_prime

    # An ASCII function which it finds the ASCII value of each character in the input value, and calculates the power of
    # 3 of the ASCII value.
    # It finally returns the value of sum of the powered values for all characters % size of the hash table.
    # This is only used as the second hash function in double hashing
    # This hash function is faster than the first one in terms of speed, with fewer collisions occur
    def hash_ascii_2(self, value):
        hash_value = 0
        for i in range(len(value)):
            hash_value += ord(value[i]) ** 5
        return hash_value % self.hash_table_size_prime

    # Polynomial hash function helps to avoid symmetry
    # This function finds the ASCII value of each character in the input value, and multiplies the ASCII value by c**i
    # (c to the power of i), which c is a constant prime number (31), and i is the index of the character in the input
    # value. It finally returns the value of sum of multiplied values for all characters % size of the hash table.
    # It is quite efficient in hashing, not many collisions occur
    def polynomial_hashing(self, value):
        c = 31
        hash_value = 0
        for i in range(len(value)):
            hash_value += ord(value[i]) * (c ** i)
        return hash_value % self.hash_table_size_prime

    # This is the resize and rehash function
    # When we cannot find a position to insert a value, or the load factor is equal or greater to 0.75, this function
    # is called
    # This function first finds the doubled value of the size of the original table, calculates the next prime number
    # of the doubled value and set it as the size of the new hash table.
    # The function create a copy table, which stores all the contents of the original table, and it initialises the
    # original table with the new size, then it loops through the copy table and insert every cell back into the resized
    # table. During inserting each cell back into the resized table, rehashing is also processing.
    def resize_and_rehash(self, value):
        self.num_rehash += 1
        # When need to rehash, double the size of the original hash table, find the next prime number of the
        # doubled value and set it as the size of the new hash table and create it by inserting the same number of cells
        # as the
        print("Now start to resize and rehash the table...")
        self.collision = 0
        self.hash_table_size = self.hash_table_size * 2
        self.hash_table_size_prime = self.nextPrime(self.hash_table_size)

        # create a new table and insert all the items from old table to new table
        self.copy_table = self.table

        # recreate and reinsert self.table
        self.table = [cell() for _ in range(self.hash_table_size_prime)]
        self.num_entries = self.hash_table_size_prime
        for item in self.copy_table:
            if item.element is not None:
                self.insert(item.element)

        self.insert(value)

    # This is the insert function, with linear probing, quadratic probing and double hashing implemented
    # If it is in mode 0, 1, 2, it will use the first hash function hash_ascii() to generate the hash
    # value; if it is in mode 4, 5, 6, it will use the second hash function polynomial_hashing() to generate the hash
    # value.
    # After the hash value is generated, we first find the relative position in the hash table by
    # self.table[hash_value], if the cell at that position is empty, we can insert the value in.
    # Otherwise, a collision occurs, we need to find the next position and try to insert the value, we use the
    # following formulae in different scenarios:
    # For linear probing, we use formula (hash(k)+i) % N.
    # For quadratic probing, we use formula (hash(k)+i**2) % N.
    # For double hashing, we call an additional hash function hash_ascii_2() to get another hash value, then we
    # use the formula (hash(k) + (i*hash2(k))) % N.
    # If we loop through the table and cannot find a space to insert the value, we rehash the table.
    def insert(self, value):
        self.start = time.time()
        # TODO code for inserting into hash table
        # determine if use ascii hash or polynomial hash
        load_factor = (self.hash_table_size_prime - self.num_entries) / self.hash_table_size_prime
        if load_factor >= 0.75:
            self.resize_and_rehash(value)
        else:
            if self.mode == HashingModes.HASH_1_LINEAR_PROBING.value:
                hash_value = self.hash_ascii(value)
                if self.table[hash_value].state == state.empty.value:
                    self.table[hash_value].element = value
                    self.table[hash_value].state = state.in_use.value
                    self.num_entries -= 1
                    self.end = time.time()
                    self.total_time += self.end - self.start
                    return True
                for i in range(1, self.hash_table_size_prime):
                    self.collision += 1
                    new_hash_value = (hash_value + i) % self.hash_table_size_prime
                    if self.table[new_hash_value].state == state.empty.value:
                        self.table[new_hash_value].element = value
                        self.table[new_hash_value].state = state.in_use.value
                        self.num_entries -= 1
                        self.end = time.time()
                        self.total_time += self.end - self.start
                        return True
                    elif self.table[new_hash_value].element == value:
                        self.end = time.time()
                        self.total_time += self.end - self.start
                        return False
                self.resize_and_rehash(value)

            elif self.mode == HashingModes.HASH_1_QUADRATIC_PROBING.value:
                hash_value = self.hash_ascii(value)
                if self.table[hash_value].state == state.empty.value:
                    self.table[hash_value].element = value
                    self.table[hash_value].state = state.in_use.value
                    self.num_entries -= 1
                    self.end = time.time()
                    self.total_time += self.end - self.start
                    return True
                for i in range(1, self.hash_table_size_prime):
                    self.collision += 1
                    new_hash_value = (hash_value + (i ** 2)) % self.hash_table_size_prime
                    if self.table[new_hash_value].state == state.empty.value:
                        self.table[new_hash_value].element = value
                        self.table[new_hash_value].state = state.in_use.value
                        self.num_entries -= 1
                        self.end = time.time()
                        self.total_time += self.end - self.start
                        return True
                    elif self.table[new_hash_value].element == value:
                        self.end = time.time()
                        self.total_time += self.end - self.start
                        return False

                return self.resize_and_rehash(value)

            elif self.mode == HashingModes.HASH_1_DOUBLE_HASHING.value:
                hash_value = self.hash_ascii(value)
                hash_value_2 = self.hash_ascii_2(value)
                if self.table[hash_value].state == state.empty.value:
                    self.table[hash_value].element = value
                    self.table[hash_value].state = state.in_use.value
                    self.num_entries -= 1
                    self.end = time.time()
                    self.total_time += self.end - self.start
                    return True
                for i in range(1, self.hash_table_size_prime):
                    self.collision += 1
                    new_hash_value = (hash_value + (i * hash_value_2)) % self.hash_table_size_prime
                    if self.table[new_hash_value].state == state.empty.value:
                        self.table[new_hash_value].element = value
                        self.table[new_hash_value].state = state.in_use.value
                        self.num_entries -= 1
                        self.end = time.time()
                        self.total_time += self.end - self.start
                        return True
                    elif self.table[new_hash_value].element == value:
                        self.end = time.time()
                        self.total_time += self.end - self.start
                        return False
                return self.resize_and_rehash(value)

            elif self.mode == HashingModes.HASH_2_LINEAR_PROBING.value:
                hash_value = self.polynomial_hashing(value)
                if self.table[hash_value].state == state.empty.value:
                    self.table[hash_value].element = value
                    self.table[hash_value].state = state.in_use.value
                    self.num_entries -= 1
                    self.end = time.time()
                    self.total_time += self.end - self.start
                    return True
                for i in range(1, self.hash_table_size_prime):
                    self.collision += 1
                    new_hash_value = (hash_value + i) % self.hash_table_size_prime
                    if self.table[new_hash_value].state == state.empty.value:
                        self.table[new_hash_value].element = value
                        self.table[new_hash_value].state = state.in_use.value
                        self.num_entries -= 1
                        self.end = time.time()
                        self.total_time += self.end - self.start
                        return True
                    elif self.table[new_hash_value].element == value:
                        self.end = time.time()
                        self.total_time += self.end - self.start
                        return False
                self.resize_and_rehash(value)

            elif self.mode == HashingModes.HASH_2_QUADRATIC_PROBING.value:
                hash_value = self.polynomial_hashing(value)
                if self.table[hash_value].state == state.empty.value:
                    self.table[hash_value].element = value
                    self.table[hash_value].state = state.in_use.value
                    self.num_entries -= 1
                    self.end = time.time()
                    self.total_time += self.end - self.start
                    return True
                for i in range(1, self.hash_table_size_prime):
                    self.collision += 1
                    new_hash_value = (hash_value + i ** 2) % self.hash_table_size_prime
                    if self.table[new_hash_value].state == state.empty.value:
                        self.table[new_hash_value].element = value
                        self.table[new_hash_value].state = state.in_use.value
                        self.num_entries -= 1
                        self.end = time.time()
                        self.total_time += self.end - self.start
                        return True
                    elif self.table[new_hash_value].element == value:
                        return False
                self.resize_and_rehash(value)

            elif self.mode == HashingModes.HASH_2_DOUBLE_HASHING.value:
                hash_value = self.polynomial_hashing(value)
                hash_value_2 = self.hash_ascii_2(value)
                if self.table[hash_value].state == state.empty.value:
                    self.table[hash_value].element = value
                    self.table[hash_value].state = state.in_use.value
                    self.num_entries -= 1
                    return True
                for i in range(1, self.hash_table_size_prime):
                    self.collision += 1
                    new_hash_value = (hash_value + (i * hash_value_2)) % self.hash_table_size_prime
                    if self.table[new_hash_value].state == state.empty.value:
                        self.table[new_hash_value].element = value
                        self.table[new_hash_value].state = state.in_use.value
                        self.num_entries -= 1
                        return True
                    elif self.table[new_hash_value].element == value:
                        return False

                return self.resize_and_rehash(value)

    # This is the find function, with linear probing, quadratic probing and double hashing implemented
    # If it is in mode 0, 1, 2, it will use the first hash function hash_ascii() to generate the hash
    # value; if it is in mode 4, 5, 6, it will use the second hash function polynomial_hashing() to generate the hash
    # value.
    # After the hash value is generated, we first find the relative position in the hash table by
    # self.table[hash_value], if the cell at that position is empty, we can insert the value in.
    # Otherwise, a collision occurs, we need to find the next position and try to insert the value, we use the
    # following formulae in different scenarios:
    # For linear probing, we use formula (hash(k)+i) % N.
    # For quadratic probing, we use formula (hash(k)+i**2) % N.
    # For double hashing, we call an additional hash function hash_ascii_2() to get another hash value, then we
    # use the formula (hash(k) + (i*hash2(k))) % N.
    # If during the process of looping the table, the cell contains None, it means the later cells found by the linear
    # probing formula will not have the value, the function can immediately return False
    # If the function finishes looping the table and still cannot find the value we want, it means the value is not in
    # the table, the function returns False
    def find(self, value):
        # TODO code for looking up in hash table
        if self.mode == HashingModes.HASH_1_LINEAR_PROBING.value:
            hash_value = self.hash_ascii(value)
            for i in range(self.hash_table_size_prime):
                new_hash_value = (hash_value + i) % self.hash_table_size_prime
                if self.table[new_hash_value].element == value:
                    return True
                elif self.table[new_hash_value].element is None:
                    return False

        elif self.mode == HashingModes.HASH_1_QUADRATIC_PROBING.value:
            hash_value = self.hash_ascii(value)
            for i in range(self.hash_table_size_prime):
                new_hash_value = (hash_value + (i ** 2)) % self.hash_table_size_prime
                if self.table[new_hash_value].element == value:
                    return True
                elif self.table[new_hash_value].element is None:
                    return False

        elif self.mode == HashingModes.HASH_1_DOUBLE_HASHING.value:
            hash_value = self.hash_ascii(value)
            hash_value_2 = self.hash_ascii_2(value)
            for i in range(self.hash_table_size_prime):
                new_hash_value = (hash_value + (i * hash_value_2)) % self.hash_table_size_prime
                if self.table[new_hash_value].element == value:
                    return True
                elif self.table[new_hash_value].element is None:
                    return False

        elif self.mode == HashingModes.HASH_2_LINEAR_PROBING.value:
            hash_value = self.polynomial_hashing(value)
            for i in range(self.hash_table_size_prime):
                new_hash_value = (hash_value + i) % self.hash_table_size_prime
                if self.table[new_hash_value].element == value:
                    return True
                elif self.table[new_hash_value].element is None:
                    return False

        elif self.mode == HashingModes.HASH_2_QUADRATIC_PROBING.value:
            hash_value = self.polynomial_hashing(value)
            for i in range(self.hash_table_size_prime):
                new_hash_value = (hash_value + (i ** 2)) % self.hash_table_size_prime
                if self.table[new_hash_value].element == value:
                    return True
                elif self.table[new_hash_value].element is None:
                    return False

        elif self.mode == HashingModes.HASH_2_DOUBLE_HASHING.value:
            hash_value = self.polynomial_hashing(value)
            hash_value_2 = self.hash_ascii_2(value)
            for i in range(self.hash_table_size_prime):
                new_hash_value = (hash_value + (i * hash_value_2)) % self.hash_table_size_prime
                if self.table[new_hash_value].element == value:
                    return True
                elif self.table[new_hash_value].element is None:
                    return False
        return False  # if we can't find the value, return false

    def print_set(self):
        # TODO code for printing hash table
        # set = []
        print("Hashset:\n")
        for i in range(len(self.table)):
            print("\t%s\n" % self.table[i].element)
            # set.append(self.table[i].element)
        # print(set)

    def print_stats(self):  # average self.collision
        # TODO code for printing statistics
        num_elements = 0
        for item in self.table:
            if item.element is not None:
                num_elements += 1
        avg_collision = self.collision / num_elements
        load_factor = num_elements / self.hash_table_size_prime
        print("Number of collisions: " + str(self.collision))
        print("Number of rehashes: " + str(self.num_rehash))
        print("Average collision per access: " + str(avg_collision))
        print("Load factor: " + str(load_factor))
        print("Total time for insert: " + str((self.total_time)*1000) + "ms")
        print("Average time per insert: " + str((self.total_time)*1000/num_elements) + "ms")




# This is a cell structure assuming Open Addressing
# It should contain and element that is the key and a state which is empty, in_use or deleted
# You will need alternative data-structures for separate chaining
class cell:
    def __init__(self):
        self.state = state.empty.value
        self.element = None
        # pass


class state(Enum):
    empty = 0
    in_use = 1
    deleted = 2


# Hashing Modes
class HashingModes(Enum):
    HASH_1_LINEAR_PROBING = 0
    HASH_1_QUADRATIC_PROBING = 1
    HASH_1_DOUBLE_HASHING = 2
    HASH_1_SEPARATE_CHAINING = 3
    HASH_2_LINEAR_PROBING = 4
    HASH_2_QUADRATIC_PROBING = 5
    HASH_2_DOUBLE_HASHING = 6
    HASH_2_SEPARATE_CHAINING = 7
