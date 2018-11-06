import sys

class DataStore(object):
	
	def __init__(self):
		
		"""
		The field below is the dictionary holding all the information about the hierarchy. The hiearchy is encoded so that the root has code "1" and to determine the child of a node's code you add "a" to the parent's node code and append the index of the child to that last "a".  The list values are the index of the node used for calling the item in the hierarchy, the nodes name or chest part name, and finally a field indicating whether the node is selected or not. 
		
		Originally I had a data structure like this plus another data m odel of a tree structure created with objects which had parent node and children references, but I thought having both the data model and dictionary going around was redundant, so I reimplemented the design so that all functions in the dataStore could act on the dictionary and my encoding. 
		"""
		
		self.dict = {"1" : [1, "Chest", False ], "1a1" : [2, "Heart", False ], "1a1a1" : [3, "Left Ventrical", False ], "1a1a2" : [4, "Right Ventrical", False ],  "1a1a3" :  [5, "Left Atrium", False ],  "1a1a4" : [6, "Right Atrium", False ], "1a1a5" : [7, "Septum", False ], "1a2": [8, "Lungs", False ], "1a2a1": [9, "Left Lung", False ], "1a2a1a1" : [10, "Superior Lobe", False ], "1a2a1a2" : [11, "Inferior Lobe", False   ], "1a2a2" : [12, "Right Lung", False ], "1a2a2a1": [13, "Superior Lobe", False ], "1a2a2a2": [14, "Middle Lobe", False ], "1a2a2a3": [15, "Inferior Lobe", False]}
		
		self.done = -1
		self.INDEX = 0
		self.NAME = 1
		self.SELECTED = 2
	
	def clearDone(self):
		self.done = -1
	"""
	This method determines whether a given number is in the dictionary store of chest parts.
	"""
	def testInListOfChest(self, str):
		test = -1
		for c in self.dict.values():
			if(test == -1):
				if(c[0] == str or c[1] == str):
					test = c[0]
			else:
				if(c[0] == str or c[1] == str):
					print("Enter in the number of the chest part as its name is not unique.")
					return -2
		return test
	
	"""
		This method determines the child's key or code based on the parent's code and the index of the child. Not 0 based numbering.
	"""
	def getChildKey(self, parent_key, child_index):
		return parent_key+"a"+str(child_index)
	
	"""
		This method obtains the parent node's code based on the child's code. 
	"""
	def getParentKey(self, key):
		if key != "1":
			return key[0:key.rfind("a")]
		return None
	
	"""
		This method is similar to the applyToDescendants method, but this method applies the func to the ancestors applying hte method func to each one. 
	"""
	def applyToAncestors(self, key, num, ret, func):
		parentKey = self.getParentKey(key)
		if parentKey != None:
			func(parentKey, num, ret)
			self.applyToAncestors( parentKey, num, ret, func)
	
	"""
		This method computes the number of direct children a node has, not including grand-... children. 
	"""	
	def computeNumberOfChildren(self, key):
		c = 0
		while self.getChildKey(key, c+1) in self.dict:
			c += 1
		return c
	
	"""
		This function is a function that takes functions as parameters. This function is used three times in three different contexts and applies functions and returns results from the traversing down the tree from a node to all its descendants. 
		
	"""
	def applyToDescendants(self, key, num, ret, func, continueFunc):
		cnt = self.computeNumberOfChildren(key)
		i = 1
		while i <= cnt and self.done == -1:
			childKey = self.getChildKey(key, i)
			tempRet = ret
			ret = func(childKey, num, ret)
			if(continueFunc(ret) == True and self.done == -1):		
				self.applyToDescendants(childKey, num, ret, func, continueFunc) 
				ret = tempRet
			else:
				self.done = ret
			i+=1

	"""
		This method is a specific case of the continueFunc used in the applyToDescendants method in this case the ultimate goal is to find the key of a dictionary item given its index that the user supplies. 
	"""
	def testIndexWithKeyContinueFunc(self, ret):
		if ret == -1:
			return True
		return False

	"""
		This method is a specific case of the func used in the applyToDescendants method in this case the ultimate goal is to find the key of a dictionary item given its index that the user supplies. 

	"""
	def testIndexWithKey(self, key, num, ret):
		if (self.dict[key])[self.INDEX] == num:
			return key
		else:
			return -1
	
	"""
		This method is the calling method using the applyToDescendants method in this case the ultimate goal is to find the key of a dictionary item given its index that the user supplies. 

	"""
	def findKeyWithIndex(self, num):
		self.done = -1
		ret = self.testIndexWithKey("1", num, "-1")	
		if self.testIndexWithKeyContinueFunc(ret) == True:
			self.applyToDescendants("1", num, ret, self.testIndexWithKey, self.testIndexWithKeyContinueFunc)
			ret = self.done
		return ret;
	
	
	
	"""
		THis method is a func for the selection of nodes used in the switchSelected - to turn an item to be selected. 
	"""		
	def selectNode(self, key, num, ret):
		(self.dict[key])[self.SELECTED] = True
	"""
	This method is a func in the deslection of nodes in the hiearchy used in the apply methods. 
	"""
	def deselectNode(self, key, num, ret):
		(self.dict[key])[self.SELECTED] = False
			
	"""
		This method is a placeholder in the selection method used in the applyToDescendants function. It is the continueFunc function. 
	"""
	def switchSelectedContinueFunc(self, ret):
		return True
	
	"""
		THis function switches the node and it's resulting ancestors or descendants from selected and deselected.
	"""	
	def switchSelected(self, key):
		self.done = -1
		if key in self.dict: 
			if (self.dict[key])[self.SELECTED] == True:
				(self.dict[key])[self.SELECTED] = False
				self.applyToDescendants(key, -1, -1, self.deselectNode, self.switchSelectedContinueFunc)
				self.done = -1
			else:
				(self.dict[key])[self.SELECTED] = True
				self.applyToAncestors(key, -1, -1, self.selectNode)
	
	"""
		This method is the func method for displaying the whole hierarchy structure used in the applyToDescendants on the root to display the hierarchy. 
	"""	
	def displayPair(self, key, num, tab):
		if (self.dict[key])[self.SELECTED] == True:
			print( tab + "[X] " + str((self.dict[key])[self.INDEX]) + ". " + (self.dict[key])[self.NAME])
		else:
			print( tab + "[ ] " + str((self.dict[key])[self.INDEX]) + ". " + (self.dict[key])[self.NAME])
		tab += "\t"
		return tab
	
	"""
		THis function is a placeholder for the continueFunc used in the display of the hierarchy. It is the continueFunc function for that case. 
	"""	
	def displayPairContinueFunc(self, ret):
		return True
	
	"""
		This function is the calling function that uses the applyToDescendants to display the whole hierarchy and its descendatns. 
	"""		
	def displayChestAndInstructions(self):
		self.done = -1
		tab = self.displayPair("1","", "")
		self.applyToDescendants("1", "", tab, self.displayPair, self.displayPairContinueFunc)
		self.done = -1