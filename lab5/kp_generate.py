# usage calling kp_generate <n> <c> <b> <name> will create a knapsack instance containing
# n items to be inserted into a knapsack of capacity c.  The profit and weight for
# each item will be a randomly generated number between 1 and b.  This will be written
# to a file called <name>
import random
import sys

n = int(sys.argv[1])
c = sys.argv[2]
b = int(sys.argv[3])
name = sys.argv[4]

fileName = name
fileObj = open(fileName,'w')
fileObj.write(str(n) + "\n")

# original
for i in range(1, n + 1):
    weight = random.randint(1, b)
    profit = random.randint(1, b)
    fileObj.write(str(i) + " " + str(profit) + " " + str(weight) + "\n")
fileObj.write(str(c))

# reverse order
# for i in range(1, n + 1):
#     weight = 3 * i
#     profit = b - i*10
#     fileObj.write(str(i) + " " + str(profit) + " " + str(weight) + "\n")
# fileObj.write(str(c))


# for i in range(1, n + 1):
#     weight = 3 * i
#     profit = b - (n+1-i)*10
#     fileObj.write(str(i) + " " + str(profit) + " " + str(weight) + "\n")
# fileObj.write(str(c))

# Capacity
# for i in range(1, n + 1):
#     weight = 2 * i
#     profit = weight * 10
#     fileObj.write(str(i) + " " + str(profit) + " " + str(weight) + "\n")
# fileObj.write(str(c))
