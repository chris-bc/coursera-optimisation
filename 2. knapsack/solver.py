#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def computeColumn(prevCol, capacity, weight, value):
#	print("computeColumn cap = " + str(capacity) + ", curItem is w" + str(weight) + ", v" + str(value))
#	print("prevcol is " + str(prevCol))
	curCol = [0]*(capacity+1)
	for k in range(0, capacity+1):
		# compare prevCol[k] to prevCol[k-weight]+value
		if k-weight >= 0 and (prevCol[k-weight] + value) > prevCol[k]:
			# Select item
			curCol[k] = prevCol[k-weight] + value
		else:
			curCol[k] = prevCol[k]

#	print("returning " + str(curCol))	
	return curCol

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    value = 0
    weight = 0
    taken = [0]*len(items)

    table = [[0]*(capacity+1) for i in range(0,item_count+1)]
	# Initialise column 0
    for column in range(1, item_count+1):
        table[column] = computeColumn(table[column-1], capacity, items[column-1].weight, items[column-1].value)
	
	# And now trace back from table[item_count][capacity] to fill taken[]
    value = table[item_count][capacity]
    weight = capacity
    
    # DEBUG
#    print(str(table))
    
    for i in range(item_count,0,-1):
        if table[i-1][weight] != table[i][weight]:
            taken[i-1] = 1
            weight -= items[i-1].weight
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

