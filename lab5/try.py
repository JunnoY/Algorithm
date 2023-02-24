capacities = [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
for capacity in capacities:
    for i in range (1,11):
        filename = "./data/" + str(capacity) + "_capacity_input_tests"+"/test"+str(i)+".txt"
        with open(filename, 'r+') as fp:
            # read an store all lines into list
            lines = fp.readlines()
            # move file pointer to the beginning of a file
            fp.seek(0)
            # truncate the file
            fp.truncate()

            # start writing lines except the first line
            # lines[1:] from line 2 to last line
            fp.writelines(lines[0:1001])

    for i in range (1,11):
        filename = "./data/" + str(capacity) + "_capacity_input_tests"+"/test"+str(i)+".txt"
        with open(filename, 'a+') as fp:
            fp.writelines(str(capacity))

