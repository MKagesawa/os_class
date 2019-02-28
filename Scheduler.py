import sys
import re

inputs = []

input_1 = sys.argv[1]
input_2 = None
isVerbose = False

class Process:
    def __init__(self, A, B, C, IO, processNum):
        self.processNum = processNum
        self.arrivalTime = int(A)
        self.maxCPUBurst = int(B)
        self.totalCPUTime = int(C)
        self.maxIOBurst = int(IO)
        self.finishTime = 0
        self.IOtime = 0
        self.runTime = 0
        self.waitTime = 0
        self.remainingQuantum = 2
        self.remainingCPUTime = int(C)
        self.CPUBurst = 0
        self.remainingIOBurst = 0
        self.status = "unstarted"
        self.processID = 0
        self.turnAroundTime = 0
        self.running = False
        self.blocked = False
        self.curWaitTime = 0

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
        sortedInput = []
        for p in inputs:
            if len(p) > 0:
                a = []
                a.append(p[0])
                a.append(p[1])
                a.append(p[2])
                a.append(p[3])
                sortedInput.append(a)
        sortedInput.sort(key=lambda x: x[0])
        print("The (sorted) input is: ", lines[0][:1], sortedInput)

else:
    with open(input_2, 'r') as f:
        lines = f.readlines()
        print("The original input was: ", lines[0])
        lines = re.sub("[^0-9 ]", "", lines[0])
        inputs.append(lines[3:].split("   "))
        inputs = inputs[0]
        for l in range(len(inputs)):
            inputs[l] = inputs[l].split()
        sortedInput = []
        for p in inputs:
            if len(p) > 0:
                a = []
                a.append(int(p[0]))
                a.append(int(p[1]))
                a.append(int(p[2]))
                a.append(int(p[3]))
                sortedInput.append(a)
        sortedInput.sort(key=lambda x: x[0])
        print("The (sorted) input is: ", lines[0][:1], sortedInput)

# make input process data to process objects

# get "random" number form file
randomNumbers = None
with open("random-numbers.txt") as f:
    randomNumbers = f.readlines()

counter = 0
def randomOS(u, counter):
    print('u', u, 'counter', counter)
    num = 1 + (int(randomNumbers[int(counter)]) % int(u))
    counter += 1
    return num

# First come first serve
def FCFS():
    print("The scheduling algorithm used was First Come First Served")
    processes = []
    readyProcess = []
    time = 0
    finished = False
    processRunning = False
    processCount = 0
    cycleCotainBlock = 0
    for p in sortedInput:
        if len(p) > 0:
            processes.append(Process(p[0], p[1], p[2], p[3], processCount))
            processCount += 1

    while (finished == False):
        readyProcess.clear()
        print("Before cycle " + str(time) + ": ", end="")
        for p in processes:
            if isVerbose:
                num = 0
                if p.status == "running":
                    num = p.remainingCPUTime
                elif p.status == "blocked":
                    num = p.remainingIOBurst
                print(p.status + str(num) + " ", end="")
        print()
        for p in processes:
            if p.status == "blocked":
                p.remainingIOBurst -= 1
                if (p.remainingIOBurst <= 0):
                    p.status = "ready"
                    p.blocked = False
                else:
                    p.blocked = True
            if p.status == "running":
                p.remainingCPUTime -= 1
                p.CPUBurst -= 1
                p.running = True
                if p.remainingCPUTime <= 0:
                    p.status = "terminated"
                    p.running = False
                    p.finishTime = time
                    p.turnAroundTime = time - p.arrivalTime
                elif p.CPUBurst <= 0:
                    p.status = "blocked"
                    p.remainingIOBurst = randomOS(p.IOtime, counter)
                    p.running = False
                    p.blocked = True
            if p.status == "unstarted" and time >= int(p.arrivalTime):
                p.status = "ready"
            if p.status == "ready":
                readyProcess.append(p)

            for p in processes:
                if p.blocked:
                    cycleCotainBlock += 1
                    break

            processRunning = False
            for p in processes:
                if p.running:
                    processRunning = True

            # choose a process to run
            if not processRunning:
                if len(readyProcess) != 0:
                    processRun = readyProcess[0]
                    del readyProcess[0]
                    for p in readyProcess:
                        if p.curWaitTime > processRun.curWaitTime:
                            processRun = p
                        elif p.arrivalTime < processRun.arrivalTime:
                            processRun = p
                        elif p.arrivalTime == processRun.arrivalTime:
                            if p.processID < processRun.processID:
                                processRun = p

                    # Increment waiting time for process not running
                    for p in readyProcess:
                        if processRun.processID != p.processID:
                            p.curWaitTime += 1

                    # Run process
                    processRun.status = "running"
                    processRun.curWaitTime = 0
                    processRun.CPUBurst = randomOS(processRun.maxCPUBurst, counter)
                    processRun.running = True

        # check if all process finished
        finished = True
        for p in processes:
            if p.status != "terminated":
                finished = False

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
# RR()
# Uniprogrammed()
# SJF()
