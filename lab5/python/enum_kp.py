import sys
import math

from knapsack import knapsack

class enum_knapsack(knapsack):
    def __init__(self, filename):
        knapsack.__init__(self, filename)
        
    def enumerate(self):
        # Do an exhaustive search (aka enumeration) of all possible ways to pack
        # the knapsack.
        # This is achived by creating every "binary" solution vectore of length Nitems.
        # For each solution vector, its value and weight is calculated
        
        solution = [False]*(self.Nitems + 1) # (binary/ true/false) solution vector representing items pack
        best_solution = [False]*(self.Nitems + 1) # (binary) solution vector for best solution found
        j = 0.0
        
        self.QUIET = True
        best_value = 0 # total value packed in the best solution
        temp_percentage = 0
        while (not self.next_binary(solution, self.Nitems)):
            j = j + 1.0
            if (not self.QUIET):
                print("done %g of the full enumeration" % (j/math.pow(2, self.Nitems)))

            infeasible = self.check_evaluate_and_print_sol(solution)
            
            if ((not infeasible) and self.total_value > best_value):
                best_value = self.total_value
                
                for i in range(1, self.Nitems + 1):
                    best_solution[i] = solution[i]

            # This is the implementation of progress bar, the progress bar updates when every 5% of the progress is done
            percentage = int((j / math.pow(2, self.Nitems)) * 100)
            if percentage % 5 == 0 and percentage != temp_percentage:
                temp_percentage = percentage
                print("Completed: [{:{}}] {:>3}%".format('=' * int(percentage / (100.0 / 30)), 30, int(percentage)))
                best_solution_array = []
                for item in best_solution:
                    if item is False:
                        best_solution_array.append(0)
                    else:
                        best_solution_array.append(1)
                print("Current best solution:", best_solution_array)

            if (not self.QUIET):
                print("best so far has value %d" % best_value)

        # This is the implementation of progress bar, print out the progress bar when the process is 100% completed
        percentage = int(round((j / math.pow(2, self.Nitems)) * 100))
        print("Completed: [{:{}}] {:>3}%".format('=' * int(percentage / (100.0 / 30)), 30, int(percentage)))

        self.QUIET = False
        print("Finished.\nPack the following items for optimal")
        self.check_evaluate_and_print_sol(best_solution)
        
    def next_binary(self, sol, Nitems):
        # Called with a "binary" vector of length Nitems, this
        # method "adds 1" to the vector, e.g. 0001 would turn to 0010.
        # If the string overflows, then the function returs True, else it returns False
        i = Nitems
        while (i > 0):
            if (sol[i]):
                sol[i] = False
                i = i -1
            else:
                sol[i] = True
                break
        if (i == 0):
            return True
        else:
            return False
        
            


knapsk = enum_knapsack(sys.argv[1])
knapsk.print_instance()
knapsk.enumerate()

