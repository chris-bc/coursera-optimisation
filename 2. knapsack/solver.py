#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

biggestTaken = []

def estimate(item, items, capacity):
	# Estimate by ordering items by value/weight and taking as many as possible
	est = 0
	remainingCap = capacity
	itemsToSort = items[item.index:]
	sortedItems = sorted(itemsToSort, key=lambda x: x.value / float(x.weight), reverse=True)
	
	for i in range(0, len(sortedItems)):		 
		if sortedItems[i].weight <= remainingCap:
			est += sortedItems[i].value
			remainingCap -= sortedItems[i].weight
		else:
			est += remainingCap * sortedItems[i].value / float(sortedItems[i].weight)
			remainingCap = 0
	return est
	
def findBestChild(item, items, capacity, value, taken, biggestValue):
	global biggestTaken
	
	# Prune immediately if capacity < 0
	if capacity < 0:
		return biggestValue
	
	# Find an estimate
	est = value + estimate(item, items, capacity)
	
	# Debug
#	print("Looking at item index " + str(item.index) + ", cap " + str(capacity) +
#		", val " + str(value) + ", biggest " + str(biggestValue) + ", est " + str(est))
			
	# Is the estimate smaller than the biggest already-found value?
	if biggestValue >= est:
		return biggestValue
	
	# Is item a leaf?
	if item.index >= len(items) - 1:
#		print("in leaf index "+str(item.index)+", taken is "+str(taken)+", biggest is "+str(biggestTaken))
		# Is there space for itemIndex?
		if capacity >= item.weight:
			# Add it if it's good
			if value + item.value > biggestValue:
				taken[item.index] = 1
				biggestTaken = copy.copy(taken)
				return value + item.value
			else:	
				# If space for item but no point adding, don't change anything
				taken[item.index] = 0
				biggestTaken = copy.copy(taken)
#				print("in leaf taken "+str(taken) + ", BT " + str(biggestTaken))
				if value > biggestValue:
					return value
				else:
					return biggestValue
		# No space - Are we a winner anyway?
		if value > biggestValue:
			taken[item.index] = 0
			biggestTaken = copy.copy(taken)
			return value
		return biggestValue
	else:
		# Compute best option if item is taken
#		print("descending the tree from item "+str(item.index))
		taken[item.index]=1
		testValue = findBestChild(items[item.index + 1], items, capacity - item.weight, value + item.value, taken, biggestValue)
		if testValue > biggestValue:
			biggestValue = testValue
		taken[item.index]=0
#		print("returned "+str(testValue)+" descending right side of tree from item "+str(item.index))
		testValue = findBestChild(items[item.index + 1], items, capacity, value, taken, biggestValue)
#		print("returned "+str(testValue))
		if testValue > biggestValue:
			biggestValue = testValue
		taken = biggestTaken
			
		return biggestValue

def solve_it(input_data):
    global biggestTaken

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
    biggestTaken = [0]*len(items)
    
    value = findBestChild(items[0], items, capacity, value, taken, value)
    taken = biggestTaken
    
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

