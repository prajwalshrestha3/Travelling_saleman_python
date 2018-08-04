import xlrd
import random
from random import shuffle
from random import randint

best_value_arr = []
best_route = []
savedIteration = 0
best_value = 10000
something = False
population = 10
cities_List = [2, 3, 4, 5, 6, 7, 8]
#creating a 2d array and filling it with 'x'
rand_pop = [['x' for i in range(7)] for j in range(10)]
#when getting the values the first item is row and the 2nd is column
data = xlrd.open_workbook('/Users/prajwalshrestha/Desktop/travelling_salesman/travelling_sales.xlsx')
worksheet = data.sheet_by_name('Sheet1')
#print(worksheet.cell(1,0).value)
#print(data.sheet_names())
for iteration in range(0,2000):
#function to calculate the initial total of the first generation population
	def calc_init_distance():
		#array to store the total distances calculated
		dist_Total = []
		#dict to store the total distance and array which holds the path it tool
		keyValue = {}
		#dict which is sorted according to the distances
		sortedKeyVal = {}
		#for loop calculate the distances from the array that is provided
		for i in range(0,population):
			total = 0
			for j in range (0,7):
				#to prevent Index Error
				if(j + 1 < len(rand_pop[1])):
					total = total + worksheet.cell(rand_pop[i][j],rand_pop[i][j + 1]).value
			#adding the distance of london to the first value of the rand_pop array because every journey starts from london and
			#also adding the distance from last destination to london
			lonToX = worksheet.cell(1, rand_pop[i][0]).value
			#storing the distance from x to london as the journey needs to end in london
			XtoLon = worksheet.cell(rand_pop[i][6],1).value
			#adding the distances from london to x and x to london
			total += (lonToX + XtoLon)
			keyValue[total] = rand_pop[i]
			#print(total)
			#creating an array to store the total distances calculated for each array in the rand_pop array
		topFiveDist = 0
		#loop that only gets the first five of the key:value pair list
		for key in sorted(keyValue.keys()):
			if(topFiveDist < 5):
				sortedKeyVal[key] = keyValue[key]
			else:
				break
			topFiveDist += 1
		best_value_arr.append(min(int(key) for key in sortedKeyVal))
		best_value = min(best_value_arr)
		if(iteration == 1999):
			print('best_value = ' + str(best_value))
		if(sortedKeyVal.get(best_value) != None):
			global string 
			global best_route 
			best_route = sortedKeyVal.get(best_value)
			print('Best route = ' + str(sortedKeyVal.get(best_value)))
		if iteration == 1999:
			print('The best route to take is: London -> ' + str(worksheet.cell(0, best_route[0]).value) + ' -> ' + str(worksheet.cell(0,best_route[1]).value) + ' -> ' + str(worksheet.cell(0,best_route[2]).value) + ' -> ' + str(worksheet.cell(0,best_route[3]).value) + ' -> ' + str(worksheet.cell(0,best_route[4]).value) + ' -> ' + str(worksheet.cell(0,best_route[5]).value) + ' -> ' + str(worksheet.cell(0,best_route[6]).value) + ' -> London')		


	def mutation():
		counter = 0
		mutation_rate = 0.05
		mutated = []
		#the key:value pair list from stored in a different variable as a duplicate
		keyValuePair = calc_init_distance()
		#the values for the keyValuePair dict stored in a list
		for values in keyValuePair.values():
			mutated.append(values) 
		#for loop to make sure that all the arrays go through a check for mutation
		for x in range(0,len(keyValuePair.values())-1):
			#random value created to check if the mutation is to be applied
			randomVal = random.random()
			#if statement that checks if the value of the randomVal is greater than the mutation rate and if it is then mutation is applied
			if(randomVal < mutation_rate):
				# two different random values that are the indexes that needs to be exchanged
				randomInList1 = randint(0,len(list(keyValuePair.values())[0])-1)
				randomInList2 = randint(0,len(list(keyValuePair.values())[0])-1)
				#print(list(keyValuePair.values())[x])
				#while loop so that the random indexes are not the same
				while(randomInList1 == randomInList2):
					randomInList2 = randint(0,len(list(keyValuePair.values())[0])-1)
				#performing the swap of random indexes
				list(keyValuePair.values())[x][randomInList1], list(keyValuePair.values())[x][randomInList2] = list(keyValuePair.values())[x][randomInList2], list(keyValuePair.values())[x][randomInList1]
				#items being added to the mutated list once the mutation is done
				mutated[x] = list(keyValuePair.values())[x]
				#print(list(keyValuePair.values())[x])
		return mutated

	def crossOver():
		#storing the array returned from the mutation function in a new array
		crossOvered = mutation()
		#making a new array with 0s inside
		newArray = [0] * 7
		#creating two random values between 0 and 4 for selecting random arrays on the Map variable
		randArr1 = randint(0,len(crossOvered)-1)
		randArr2 = randint(0,len(crossOvered)-1)
		#while loop so check and change if the two random values are the same as we dont want to select the same two arrays
		while(randArr1 == randArr2):
			randArr2 = randint(0,len(crossOvered)-1)
		array1 = crossOvered[randArr1]
		array2 = crossOvered[randArr2]
		#random index is picked from an array
		getRindex = randint(0,len(crossOvered[0])-2)
		#replacing the value of one of the 0s in the position getRindex to the value of array1[getRindex]
		newArray[getRindex] = array1[getRindex]
		#increasing the value of getRindex by one so that the 2nd 0 value can be replace by the next value of array1
		getRindex += 1
		newArray[getRindex] = array1[getRindex]
		#increasing the value again so that the replacing of the 0s starts from the index next to the value that has already been filled
		getRindex += 1
		#preventing index error
		if(getRindex > 6):
			getRindex = 0
		#skips valriable is used in the loop below 
		skips = 0
		#while loop that continues until all the 0 values are filled
		while(0 in newArray):
			#while loop that checks if there are any duplicates given therere are no index errors
			while(array2[getRindex] in newArray):
				#preventing index error
				if(getRindex + 1 == 7):
					getRindex = 0
				else:
					getRindex += 1
				#skips variable is used to keep the index of the newArray the same when the index of the array2 changes
				skips += 1
			#replacing the 0s after the duplicate value has been skipped
			newArray[getRindex - skips] = array2[getRindex]
			#increasing the index so that other 0s can be replaced
			getRindex += 1
			if(getRindex > 6):
				getRindex = 0
		#print(crossOvered)
		#print('new Array = ' + str(newArray))
		crossOvered.append(newArray)
		return crossOvered

	# if the first iteration has finished then the new population needs to be allocated
	if something == False:
			#nested loop that runs to create a 2d array with shuffled numbers
		for x in range(population):
			#shuffling the list to find the first 10 inidividuals
			shuffle(cities_List)
			shuffle_it = cities_List
			for y in range(len(cities_List)):
				#creating 2d array to save all the random value list created so that the total distances can be calculated for each list
				rand_pop[x][y] = shuffle_it[y]
	#when the first iteration has finished create population of 10 with the ones that were the best from the last generation
	else:
		nextGen = crossOver()
		for x in range(0,3):
			#shuffling the list to find the first 10 inidividuals
			shuffle(cities_List)
			shuffle_it = cities_List
			nextGen.append(shuffle_it)
		rand_pop = nextGen
	calc_init_distance()
