import sys
import re

inputs = []

input_1 = sys.argv[1]
input_2 = None
isVerbose = False

if input_1 == "--verbose":
    isVerbose = True
    input_2 = sys.argv[2]

if input_2 is None:
    with open(input_1, 'r') as f:
        lines = f.readlines()
        print("The original input was: ", lines[0])
        lines = re.sub("[^0-9 ]", "", lines[0])
        inputs.append(lines[3:].split("   "))
        inputs = inputs[0]
        for l in range(len(inputs)):
            inputs[l] = inputs[l].split()
else:
    with open(input_2, 'r') as f:
        lines = f.readlines()
        print("The original input was: ", lines[0])
        lines = re.sub("[^0-9 ]", "", lines[0])
        inputs.append(lines[3:].split("   "))
        inputs = inputs[0]
        for l in range(len(inputs)):
            inputs[l] = inputs[l].split()


class Process:
    def __init__(self, A, B, C, IO, processNum):
        self.processNum = processNum
        self.arrivalTime = A
        self.maxCPUBurst = B
        self.totalCPUTime = C
        self.maxIOBurst = IO
        self.finishTime = 0
        self.IOtime = 0
        self.runTime = 0
        self.waitTime = 0
        self.remainingQuantum = 2
        self.remainingCPUTime = C
        self.CPUBurst = 0
        self.remainingIOBurst = 0
        self.status = "notstarted"
        self.processID = 0
        self.turnAroundTime = 0


# make input process data to process objects

# get "random" number form file
randomNumbers = None
with open("random-numbers.txt") as f:
    randomNumbers = f.readlines()

counter = 0
def randomOS(u):
    return 1 + (randomNumbers[counter] % u)

# First come first serve
def FCFS():
    print("The scheduling algorithm used was First Come First Served")
    processes = []
    readyProcess = []
    time = 0
    finished = False
    currentRunning = None
    processCount = 0
    cycleCotainBlock = 0
    for p in inputs:
        if len(p) > 0:
            processes.append(Process(p[0], p[1], p[2], p[3], processCount))
            processCount += 1

    while (finished == False):
        readyProcess.clear()
        for p in processes:
            if isVerbose:
                print("Before cycle " + str(time) + ": " + p.status)
            if p.status == "blocked":
                p.remainingIOBurst -= 1
                if (p.remainingIOBurst <= 0):
                    p.status = "ready"
                    readyProcess.append(p)
            if p.status == "running":
                currentRunning = p
                p.remainingCPUTime -= 1
                p.CPUBurst -= 1
                if p.remainingCPUTime <= 0:
                    p.status = "terminated"
                    p.finishTime = time
                    p.turnAroundTime = time - p.arrivalTime
                elif p.CPUBurst <= 0:
                    p.status = "blocked"
                    p.remainingIOBurst = randomOS(p.IOtime)
            if p.status == "notstarted" and time >= int(p.arrivalTime):
                p.status = "ready"
                readyProcess.append(p)
        for p in processes:
            if p.status == "blocked":
                cycleCotainBlock += 1
        time += 1

    totalRunTime = 0
    avgTurnaround = 0
    avgWaiting = 0
    finishTime = time - 1
    for p in processes:
        print("Process ", p.processNum)
        print("(A, B, C, IO) = (", p.arrivalTime, ",", p.maxCPUBurst, ",", p.remainingCPUTime, ",", p.maxIOBurst, ")")
        print("Finishing time: ", p.finishTime)
        print("Turnaround time: ", p.turnAroundTime)
        print("Waiting time: ", p.waitTime)
        totalRunTime += p.runTime
        avgTurnaround += p.turnAroundTime
        avgWaiting += p.waitTime

    print("Finishing time: ", finishTime)
    print("CPU Utilization: ", totalRunTime/finishTime)
    print("I/O Utilization: ", cycleCotainBlock/finishTime)
    print("Throughput: ", (100 / finishTime * len(processes)), "processes per hundred cycles")
    print("Average turnaround time: ", avgTurnaround/len(processes))
    print("Average waiting time: ", avgWaiting/len(avgWaiting))


# Round Robin
def RR():
    print("The scheduling algorithm used was Round Robbin")
    pass


def Uniprogrammed():
    print("The scheduling algorithm used was Uniprocessor")

    pass


# Shortest execution time first
def SJF():
    print("The scheduling algorithm used was Shortest Job First")
    pass


FCFS()
RR()
Uniprogrammed()
SJF()
