import sys

from knapsack import knapsack

DOUB_MAX = 10e30  # a large number, must be greater than  max value of any solution
SIZE = 100000  # an estimate of how large the priority queue should become
NITEMS = 2000  # an upper limit of the number of items


class struc_sol:
    def __init__(self):
        self.solution_vec = [None] * (NITEMS + 1)  # "binary" solution vector
        # solution_vec[1] = True means first item is packed in knapsack
        # solution_vec[1] = False means first item is NOT in knapsack
        # soultion_vec[0] is meaningless

        # objects of this class will also have self.val, self.bound and self.fixed for the value, upper bound of the solutoin and number of items fixed to either True (1) or False (0), not '*"

    def copy(self):
        copy = struc_sol()
        for i in range(0, NITEMS + 1):
            copy.solution_vec[i] = self.solution_vec[i]
        copy.val = self.val
        copy.fixed = self.fixed
        copy.bound = self.bound
        return copy


class bnb(knapsack):
    def __init__(self, filename):
        knapsack.__init__(self, filename)
        self.QueueSize = 0  # the number of items currently stored in the priority queue
        self.QUIET = False  # can be set of 1 to suppress output

    # The following four functions implement a priority queue
    # They are based on the functions given in Robert Sedgwick's book, Algorithms in C

    # Discussion
    # The following four functions upheap, insert, downheap, removeMax show we used priority queue
    # insert is used to insert a structure solution in the priority queue
    # insert then calls upheap to reorder the priority queue so the structure solution with max upper bound is at the
    # front of the queue

    # removeMax removes the front structure solution which has the max upper bound from the priority queue
    # removeMax then calls downheap so the next structure solution with max upper bound in the priority queue will
    # be moved to the front of the priority queue
    def upheap(self, qsize):
        # upheap reorders the elements in the heap (queue) after an insertion

        temp_element = self.pqueue[qsize]
        self.pqueue[0].bound = DOUB_MAX

        while (self.pqueue[qsize // 2].bound <= temp_element.bound):
            self.pqueue[qsize] = self.pqueue[qsize // 2]
            qsize = qsize // 2
        self.pqueue[qsize] = temp_element

    def insert(self, element):
        assert (self.QueueSize < SIZE - 1)
        self.QueueSize = self.QueueSize + 1
        self.pqueue[self.QueueSize] = element
        self.upheap(self.QueueSize)

    def downheap(self, qindex):
        # down heap reorders the elements in the heap (queue) after a removal

        temp_element = self.pqueue[qindex]
        while (qindex <= self.QueueSize // 2):
            j = qindex + qindex
            if (j < self.QueueSize and self.pqueue[j].bound < self.pqueue[j + 1].bound):
                j = j + 1
            if (temp_element.bound >= self.pqueue[j].bound):
                break
            self.pqueue[qindex] = self.pqueue[j]
            qindex = j
        self.pqueue[qindex] = temp_element

    def removeMax(self):
        head = self.pqueue[1]
        self.pqueue[1] = self.pqueue[self.QueueSize]
        self.QueueSize = self.QueueSize - 1
        self.downheap(1)
        return head

    # End priority queue functions

    def print_sol(self, sol):
        # prints a solution in the form 000100xxx etc
        # with x's denoting the part of the solution not yet fixed (determined)

        print("%d %g " % (sol.val, sol.bound), end="")
        for i in range(1, sol.fixed + 1):
            if (sol.solution_vec[i]):
                s = "1"
            else:
                s = "0"
            print(s, end="")
        for i in range(sol.fixed + 1, self.Nitems + 1):
            print("x", end="")
            i = i + 1;
        print("")

    def frac_bound(self, sol, fix):
        # Updates the values sol.val and sol.bound

        # Computes the fractional knapsack upper bound
        # given a binary vector of items (sol->solution_vec),
        # where the first
        # "fix" of them are fixed. All that must be done
        # is compute the value of the fixed part; then
        # add to that the value obtained by adding in
        # items beyond the fixed part until the capacity
        # is exceeded. For the exceeded capacity, the fraction
        # of the last item added which would just fill the knapsack
        # is taken. This fraction of profit/value is added to the
        # total. This is the required upper bound.

        # Everything above assumes items are sorted in decreasing
        # profit/weight ratio


        #Discussion
        # frac_bound is a function that takes the sol and fix as inputs
        # sol is the current solution, which is an array of boolean values, each index position represents an item
        # if we decide take the item represented by index i, sol[i] = True
        # if we decide not to take the item represented by index i, sol[i] = False
        # if we have not decided whether we should take the item represented by index i, sol[i] = None
        # fix is the number of items that we have decided whether we should take them or not

        # frac_bound takes the inputs and computes the value of profit that the solution currently gives, and it
        # also computes the upper bound of the solution which is the maximum profit the solution could give
        # when it is fully completed (feasible)

        # partial solution is the solution vector which only parts of the elements have been assigned to True or False
        # we still need to loop through this solution vector to determine the boolean value for the rest of the elements

        # feasible solution is the solution vector that is fully computed, which gives us a complete selection of items
        # that we can take without exceeding the capacity of the knapsack
        # There is no more element that we need to determine a boolean value for it in a feasible solution vector
        totalp = 0  # profit total
        totalw = 0  # weight total
        sol.val = -1

        # compute the current value and weight of the fixed part
        for i in range(1, fix + 1):
            if (sol.solution_vec[i]):
                totalw = totalw + self.item_weights[self.temp_indexes[i]]
                totalp = totalp + self.item_values[self.temp_indexes[i]]
        if (totalw > self.Capacity):
            return

        sol.val = totalp
        #   print("%g %d" % (totalp, totalw))

        # add in items the rest of the items until capacity is exceeded
        i = fix + 1
        while (i <= self.Nitems and totalw < self.Capacity):
            # ADD CODE HERE to update totalw and totalp
            totalp = totalp + self.item_values[self.temp_indexes[i]]
            totalw = totalw + self.item_weights[self.temp_indexes[i]]
            i = i + 1

        # if over-run the capacity, adjust profit total by subtracting that overrun fraction of the last item
        if (totalw > self.Capacity):
            i = i - 1
            totalp = totalp - ((totalw - self.Capacity) / (self.item_weights[self.temp_indexes[i]]) * self.item_values[
                self.temp_indexes[i]])
        sol.bound = totalp

    def branch_and_bound(self, final_sol):
        self.pqueue[0] = struc_sol()  # set a blank first element
        # branch and bound

        # start with the empty solution vector
        # compute its value and its bound
        # put current_best = to its value
        # store it in the priority queue

        # LOOP until queue is empty or upper bound is not greater than current_best:
        #   remove the first item in the queue
        #   construct two children, 1 with a 1 added, 1 with a O added
        #   FOREACH CHILD:
        #     if infeasible, discard child
        #     else
        #       compute the value and bound
        #       if value > current_best, set current_best to it, and copy child to final_sol
        #       add child to the queue
        # RETURN

        # YOUR CODE GOES HERE
        empty_sol = struc_sol()
        empty_sol.solution_vec[0] = False
        empty_sol.fixed = 0  # at the beginning, the number of items fixed to either True (1) or False (0) is 0
        self.frac_bound(empty_sol, empty_sol.fixed)
        current_best = empty_sol.val
        self.insert(empty_sol)
        upper_bound = empty_sol.bound
        while self.QueueSize > 0 and upper_bound > current_best:
            head = self.removeMax()
            upper_bound = head.bound

            # create the first child which False is added
            child_a = head.copy()
            child_a.fixed += 1
            child_a.solution_vec[child_a.fixed] = True

            # create the second child which False is added
            child_b = head.copy()
            child_b.fixed += 1
            child_b.solution_vec[child_b.fixed] = False

            # find the sum of items in child_a and in child_b
            sum_weight_a = 0
            sum_weight_b = 0

            for i in range(1, child_a.fixed + 1):
                if child_a.solution_vec[i] is True:
                    sum_weight_a += self.item_weights[self.temp_indexes[i]]
            for i in range(1, child_b.fixed + 1):
                if child_b.solution_vec[i] is True:
                    sum_weight_b += self.item_weights[self.temp_indexes[i]]

            # Discussion
            # We used priority queue here
            # The code self.insert is a function that insert objects into the priority queue
            # For example, self.insert(child_a) inserts a structure solution child_a into the priority queue
            # which contains solution vectors, then insert will call a function called upheap, which reorders
            # all the structure in it based on their bound
            # The higher upper bound the structure solution has, the closer the structure solution to
            # the front of the priority queue

            # Check feasibility
            if sum_weight_a <= self.Capacity:
                self.frac_bound(child_a, child_a.fixed)
                if child_a.val > current_best:
                    current_best = child_a.val
                    self.copy_array(child_a.solution_vec, final_sol)
                    self.insert(child_a)
                if child_a.bound > upper_bound:
                    upper_bound = child_a.bound
                self.insert(child_a)

            if sum_weight_b <= self.Capacity:
                self.frac_bound(child_b, child_b.fixed)
                if child_b.val > current_best:
                    current_best = child_b.val
                    self.copy_array(child_b.solution_vec, final_sol)
                if child_b.bound > upper_bound:
                    upper_bound = child_b.bound
                self.insert(child_b)
            print("Current best solution=" + str(current_best))

    def copy_array(self, array_from, array_to):
        # This copies Nitems elements of one boolean array to another
        # Notice it ignores the 0th item of the array
        for i in range(1, self.Nitems + 1):
            array_to[i] = array_from[i]


knapsk = bnb(sys.argv[1])
assert (NITEMS >= knapsk.Nitems)
final_sol = [False] * (knapsk.Nitems + 1)
knapsk.sort_by_ratio()

# We used priority queue, the following initialises a priority queue of size = 100000
knapsk.pqueue = [None] * SIZE

knapsk.branch_and_bound(final_sol)
print("Branch and Bound Solution of Knapack is:")
knapsk.check_evaluate_and_print_sol(final_sol)
