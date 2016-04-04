from time import time
from Queue import PriorityQueue
from operator import itemgetter
import random

class WaitNICPriorityQueue(PriorityQueue): #Create class for making the priority waiting of NIC Queue#
	def __init__(self):
		PriorityQueue.__init__(self)
	def put(self, item):
		PriorityQueue.put(self, (item.priority, item))
	def get(self, *args, **kwargs):
		_, _, item = PriorityQueue.get(self, *args, **kwargs)
		return item

class ProcessClass: #create class ProcessClass in order to compute the waiting time#
	priority = 0  #Initializing#
	waitTime = 0   #Initializing#
	countNIC = 0    #Initializing#
	runTime = 0.0    #Initializing#
	tempRunTime = 0.0  #Initializing#
	pendingNIC = 0    #Initializing#
	pID = 0         #Initializing#
	def __init__(self, priority, pID):
		self.priority = priority 
		self.pendingNIC = 1
		self.pID = pID
	def executeOther(self, waitNIC): 
		if(self.pendingNIC):
			self.tempRunTime = random.expovariate(1 / 0.1) #caluclation for Exponential distribution  Lambda and Mu#
			self.runTime = self.runTime + self.tempRunTime #calculation for run time#
			self.pendingNIC = 0
			return self.tempRunTime
		else:
			self.waitTime = self.waitTime + waitNIC #calculation for wait time#
			self.runTime = self.runTime + waitNIC  #calculation for run time#

def timeToWaitOnNIC(): #for the calculation of Time waiting on NIC
	return random.expovariate(1 / 0.1) + random.expovariate(1 / 0.1) + random.expovariate(1 / 0.1) + random.expovariate(1 / 0.1) + random.expovariate(1 / 0.1)

def main():
	startTime = time()

	#Code Starts
	
	#Consts
	TOTAL_PROCESSES = 50000
	
	#Inits
	globalRunTime = 0.0
	totalNICRunTime = 0.0
	processesProcessedNIC = 0
	processes = [ProcessClass(3, 1), ProcessClass(3, 2), ProcessClass(2, 3), ProcessClass(2, 4), ProcessClass(1, 5)]
	waitQueueNIC = PriorityQueue()
	NICwaitTime = 0

	#Code
	while True:
	#if True:
		for x in xrange(0, 5):
			processes[x].executeOther(NICwaitTime)
		totalProcessRunTime = sorted([[processes[0], processes[0].runTime], [processes[1], processes[1].runTime], [processes[2], processes[2].runTime], [processes[3], processes[3].runTime], [processes[4], processes[4].runTime]], key=itemgetter(1)) 
		globalRunTime = totalProcessRunTime[0][1]
		for x in xrange(0, 5):

			if processes[x].runTime <= globalRunTime :
				waitQueueNIC.put((processes[x].priority,processes[x]))
		unqueuedProc = waitQueueNIC.get()
		NICwaitTime = timeToWaitOnNIC()
		totalNICRunTime = totalNICRunTime + NICwaitTime
		unqueuedProc[1].pendingNIC = 1
		unqueuedProc[1].countNIC = unqueuedProc[1].countNIC + 1
		unqueuedProc[1].runTime = unqueuedProc[1].runTime + NICwaitTime
		globalRunTime = globalRunTime + NICwaitTime
		processesProcessedNIC = processesProcessedNIC + 1
		
		if processesProcessedNIC == TOTAL_PROCESSES:
			break

 	#Output Starts
	print "Fraction NIC Busy: " + str(totalNICRunTime / globalRunTime)
	print "Simulation EndTime: " + str(globalRunTime)
	for x in xrange(0, 5):
		print "The Process " + str(processes[x].pID) + " has used NIC " + str(processes[x].countNIC) + " times"

	for x in xrange(0, 5):
		print "The Process " + str(processes[x].pID) + " on Avg. Waited " + str(processes[x].waitTime/processes[x].countNIC)

	#Code Ends
	print "The code took " + str(time() - startTime) + " seconds To run"
main()
