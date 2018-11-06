import cohesicTestNode as cnode
import sys

dataStore = cnode.DataStore()
#Display hierarchy to user. 
dataStore.displayChestAndInstructions()
try:
	#Obtain user input.
	choice = input("> ")
	#Continual loop to repeatedly display hierarchy, changes, and to await new input.
	while choice != 'q' and choice != 'Q':
		#Test if num is an index in the tree. 
		num = dataStore.testInListOfChest(int(choice))
		if num >= 0:
			# the user friendly number supplied to a key
			key = dataStore.findKeyWithIndex(num)
			#print(num)
			#print (key)
			#Act on the valid input by altering the selection state. 
			dataStore.switchSelected(key)
		print ("Enter in a number or 'Q' to quit.")
		#Repeat
		dataStore.displayChestAndInstructions()
		choice = input("> ")
except ValueError:
    print("Please supply integer arguments or a 'q' to quit.")



	
	
		
		
		
		