import unittest
import cohesicTestNode as cnode

dataStore = cnode.DataStore()

def testInListOfChest(x):
	ret = dataStore.testInListOfChest(x)
	dataStore.clearDone()
	return ret

def testFindKeyWithIndex(x):
	ret = dataStore.findKeyWithIndex(x)
	dataStore.clearDone()
	return ret
	


	
class MyTest(unittest.TestCase):
	
	def test_1(self):
		self.assertEqual(testInListOfChest(3),3)
		self.assertEqual(testInListOfChest(-1),-1)
		self.assertEqual(testInListOfChest(13),13)
		self.assertEqual(testInListOfChest(100),-1)
		
	def test_2(self):
		self.assertEqual(testFindKeyWithIndex(3),"1a1a1")
		self.assertEqual(testFindKeyWithIndex(-1),-1)
		self.assertEqual(testFindKeyWithIndex(5),"1a1a3")
		self.assertEqual(testFindKeyWithIndex(8),"1a2")
		self.assertEqual(testFindKeyWithIndex(10),"1a2a1a1")
		self.assertEqual(testFindKeyWithIndex(12),"1a2a2")
		self.assertEqual(testFindKeyWithIndex(100),-1)
	
	def helperTestDeSelectedDescendants(self, key, num, ret):
		if (dataStore.dict[key])[dataStore.SELECTED] == True:
			self.assertEqual(1, -1)

	def helperTestFuncContinueTestDeselectedDescendants(self, ret):
		return True
			
	def helperTestSelectedAncestors(self, key, num, ret):
		if (dataStore.dict[key])[dataStore.SELECTED] == False:
			self.assertEqual(1, -1)
				
	def helperTestSwitchSelected(self, key1, key2):
		dataStore.clearDone()
		dataStore.switchSelected(key1)
		dataStore.clearDone()
		dataStore.applyToAncestors(key1, -1, -1, self.helperTestSelectedAncestors)
		dataStore.clearDone()
		self.assertEqual(1,1)
		dataStore.switchSelected(key2)
		dataStore.clearDone()
		dataStore.applyToDescendants(key2, -1, -1, self.helperTestDeSelectedDescendants, self.helperTestFuncContinueTestDeselectedDescendants)
		dataStore.clearDone()
		self.assertEqual(1,1)

	
	def test_3(self):
		self.helperTestSwitchSelected("1a1a3","1a1")
		self.helperTestSwitchSelected("1a2a2a2","1a2")

		
		
suite = unittest.TestLoader().loadTestsFromTestCase(MyTest)
unittest.TextTestRunner(verbosity=2).run(suite)
		
	