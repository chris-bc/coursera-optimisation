#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def estimate(item, items, capacity):
	# Dumb estimate ignoring constraint
	est = 0
	for i in range(item.index, len(items)):
		est += items[i].value
	return est
	
def findBestChild(item, items, capacity, value, taken, biggestValue):
	# Find an estimate
	est = value + estimate(item, items, capacity)
	
	# Debug
	print("Looking at item index " + str(item.index) + ", cap " + str(capacity) +
		", val " + str(value) + ", biggest " + str(biggestValue) + ", est " + str(est))
			
	# Is the estimate smaller than the biggest already-found value?
	if biggestValue >= est:
		taken[item.index] = 0
		return biggestValue
	
	# Is item a leaf?
	if item.index >= len(items) - 1:
		# Is there space for itemIndex?
		if capacity >= item.weight:
			# Add it if it's good
			if value + item.value > biggestValue:
				taken[item.index] = 1
				return value
			
		else:
			# If no space for item, or space but no point adding, don't change anything
			taken[item.index] = 0
			if value > biggestValue:
				return value
			else:
				return biggestValue
	else:
		# Compute best option if item is taken
		takenTaken = taken
		notTakenTaken = taken
		takenValue = findBestChild(items[item.index + 1], items, capacity - item.weight, value + item.value, takenTaken, biggestValue)
		notTakenValue = findBestChild(items[item.index + 1], items, capacity, value, notTakenTaken, biggestValue)
		
		if takenValue  > notTakenValue and takenValue > biggestValue:
			# TODO: Fix the intermediate levels of taken ... takenTaken etc.
			taken[item.index] = 1
			biggestValue = takenValue
		if notTakenValue > takenValue and notTakenValue > biggestValue:
			biggestValue = notTakenValue
			taken[item.index] = 0
			
		return biggestValue

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
    
    value = findBestChild(items[0], items, capacity, value, taken, value)
    
    
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

