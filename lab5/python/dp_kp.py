import sys

from knapsack import knapsack

class dp(knapsack):
    def __init__(self, filename):
        knapsack.__init__(self, filename)
        
    def DP(self, solution):
        # Renaming things to keep track of them wrt. names used in algorithm
        v = self.item_values;
        wv = self.item_weights;
        n = self.Nitems
        W = self.Capacity
        # the dynamic programming function for the knapsack problem
        # the code was adapted from p17 of http://www.es.ele.tue.nl/education/5MC10/solutions/knapsack.pdf

        # v array holds the values / profits / benefits of the items
        # wv array holds the sizes / weights of the items
        # n is the total number of items
        # W is the constraint (the weight capacity of the knapsack)
        # solution: True in position n means pack item number n+1. False means do not pack it.
        
        # V and Keep should be 2d arrays for use in the dynamic programming solution
        # The are both of size (n + 1)*(W + 1)
        
        # Initialise V and keep
        # ADD CODE HERE

        # Discussion
        # Initialise 2d array V of size (n + 1)*(W + 1) with value = 0 at every index position
        # Each row in V represents one of the n items (nth row represents the nth item)
        # Each column in V represents the capacity of the knapsack (starts from 0 to W)
        #The value stored at position V[row][column] is the optimal profit obtained by having
        # the item at the current row and all its previous items with the knapsack capacity
        # represented by the column value.
        V = [[0] * (W+1) for i in range(n+1)]

        # Discussion
        # Initialise 2d array Keep of size (n + 1)*(W + 1) with value = 0 at every index position
        # Each row in Keep represents one of the n items (nth row represents the nth item)
        # Each column in Keep represents the capacity of the knapsack (starts from 0 to W)
        # The value stored at position Keep[row][column] is a boolean value (0 or 1)
        # The boolean value shows whether we keep the item represented by the current row,
        # with the knapsack capacity represented by the current column
        # If Keep[row][column] = 1, that means we keep the item.
        # If Keep[row][column] = 0, that means we do not keep the item
        Keep = [[0] * (W+1) for i in range(n+1)]
        
        # Set the values of the zeroth row of the partial solution table to False
        # ADD CODE HERE
        for w in range(W+1):
            V[0][w] = 0
        # main dynamic programming loops, adding an item at a time and looping through weights from 0 to W
        # ADD CODE HERE
        for i in range(1, n+1):
            for w in range(W+1):
                # Discussion
                # check if the current total item weight exceeds the knapsack weight and check if the optimal value
                # of the current item will be greater than the optimal value of its previous item
                if wv[i] <= w and v[i] + V[i-1][w-wv[i]] > V[i-1][w]:
                    V[i][w] = v[i] + V[i-1][w-wv[i]]
                    Keep[i][w] = 1  # set Keep[i][w] = 1 means we keep this item i with knapsack capacity = w
                else:
                    V[i][w] = V[i-1][w]
                    Keep[i][w] = 0 # set Keep[i][w] = 0 means we do not keep this item i with knapsack capacity = w
        # now discover which items were in the optimal solution
        # ADD CODE HERE
        K = W
        for i in range(n, 0, -1):
            # Discussion
            # We can loop through Keep to search for the indexes i which Keep[i][K] = 1,
            # which means we should keep the item with knapsack weight = K
            # We can use the index i to set solution[i] = True, so this item is included in our solution
            if Keep[i][K] == 1:
                solution[i] = True
                K = K - wv[i]
        return V[n][W]
        
knapsk = dp(sys.argv[1])
solution = [False]*(knapsk.Nitems + 1)
knapsk.DP(solution);
knapsk.check_evaluate_and_print_sol(solution)
