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
    num = 1 + (int(randomNumbers[int(counter)]) % int(u))
    # print(int(randomNumbers[int(counter)]))
    # print(num)
    return num

# First come first serve
def FCFS():
    processes = []
    readyProcess = []
    time = 0
    finished = False
    processCount = 0
    cycleContainBlock = 0
    global counter
    counter = 0
    for p in sortedInput:
        if len(p) > 0:
            processes.append(Process(p[0], p[1], p[2], p[3], processCount))
            processCount += 1

    while (finished == False):
        readyProcess.clear()
        if isVerbose:
            print("Before cycle " + str(time) + ": ", end="")
        readyProcess.clear()
        for p in processes:
            if isVerbose:
                num = 0
                if p.status == "running":
                    num = p.CPUBurst
                elif p.status == "blocked":
                    num = p.remainingIOBurst
                print(p.status + " " + str(num) + " ", end="")
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
                    p.remainingIOBurst = randomOS(p.maxIOBurst, counter)
                    counter += 1
                    p.running = False
                    p.blocked = True
            if p.status == "unstarted" and time >= int(p.arrivalTime):
                p.status = "ready"
            if p.status == "ready":
                readyProcess.append(p)

        processRunning = False
        for p in processes:
            if p.running:
                processRunning = True

        for p in processes:
            if p.blocked:
                cycleContainBlock += 1
                break

        # choose a process to run
        if not processRunning:
            if len(readyProcess) != 0:
                processRun = readyProcess[0]
                for p in readyProcess:
                    if p.arrivalTime < processRun.arrivalTime:
                        processRun = p
                    elif p.curWaitTime > processRun.curWaitTime:
                        processRun = p
                    # elif p.arrivalTime == processRun.arrivalTime:
                    #     if p.processID < processRun.processID:
                    #         processRun = p

                # Increment waiting time for process not running
                for p in readyProcess:
                    if processRun != p:
                        p.curWaitTime += 1
                        # print("pID", p.processNum, "curwait", p.curWaitTime)

                # Run process
                processRun.status = "running"
                processRun.curWaitTime = 0
                processRun.CPUBurst = randomOS(processRun.maxCPUBurst, counter)
                counter += 1
                processRun.running = True

        for p in processes:
            if p.status == "ready":
                p.waitTime += 1
            if p.status == "blocked":
                p.IOtime += 1

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
    print("The scheduling algorithm used was First Come First Served")
    for p in processes:
        print("Process ", p.processNum, ":")
        print("\t(A, B, C, IO) = (", p.arrivalTime, ",", p.maxCPUBurst, ",", p.totalCPUTime, ",", p.maxIOBurst, ")")
        print("\tFinishing time: ", p.finishTime)
        print("\tTurnaround time: ", p.turnAroundTime)
        print("\tI/O time: ", p.IOtime)
        print("\tWaiting time: ", p.waitTime)
        totalRunTime += p.totalCPUTime
        avgTurnaround += p.turnAroundTime
        avgWaiting += p.waitTime

    print("Suymmary Data: ")
    print("\tFinishing time: ", finishTime)
    print("\tCPU Utilization: ", totalRunTime/finishTime)
    print("\tI/O Utilization: ", cycleContainBlock/finishTime)
    print("\tThroughput: ", (100 / finishTime * len(processes)), "processes per hundred cycles")
    print("\tAverage turnaround time: ", avgTurnaround/len(processes))
    print("\tAverage waiting time: ", avgWaiting/len(processes))


# Round Robin
def RR():
    processes = []
    readyProcess = []
    time = 0
    finished = False
    processCount = 0
    cycleContainBlock = 0
    global counter
    counter = 0
    for p in sortedInput:
        if len(p) > 0:
            processes.append(Process(p[0], p[1], p[2], p[3], processCount))
            processCount += 1

    while (finished == False):
        if isVerbose:
            print("Before cycle " + str(time) + ": ", end="")
        for p in processes:
            if isVerbose:
                num = 0
                if p.status == "running":
                    num = p.CPUBurst
                elif p.status == "blocked":
                    num = p.remainingIOBurst
                print(p.status + " " + str(num) + " ", end="")
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
                p.remainingQuantum -= 1
                p.running = True
                if p.remainingCPUTime <= 0:
                    p.status = "terminated"
                    p.running = False
                    p.finishTime = time
                    p.turnAroundTime = time - p.arrivalTime
                elif p.CPUBurst <= 0:
                    p.status = "blocked"
                    p.remainingIOBurst = randomOS(p.maxIOBurst, counter)
                    counter += 1
                    p.running = False
                    p.blocked = True
                elif p.remainingQuantum <= 0:
                    p.status = "ready"
            if p.status == "unstarted" and time >= int(p.arrivalTime):
                p.status = "ready"
            if p.status == "ready" and p not in readyProcess:
                readyProcess.append(p)

        processRunning = False
        for p in processes:
            if p.running:
                processRunning = True

        for p in processes:
            if p.blocked:
                cycleContainBlock += 1
                break

        # choose a process to run
        if not processRunning:
            if len(readyProcess) != 0:
                processRun = readyProcess.pop(0)

                # Increment waiting time for process not running
                for p in readyProcess:
                    if processRun != p:
                        p.curWaitTime += 1

                # Run process
                processRun.status = "running"
                processRun.curWaitTime = 0
                processRun.CPUBurst = max(randomOS(processRun.maxCPUBurst, counter), 2)
                counter += 1
                processRun.running = True

        for p in processes:
            if p.status == "ready":
                p.waitTime += 1
            if p.status == "blocked":
                p.IOtime += 1

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
    print("The scheduling algorithm used was Round Robbin")
    for p in processes:
        print("Process ", p.processNum, ":")
        print("\t(A, B, C, IO) = (", p.arrivalTime, ",", p.maxCPUBurst, ",", p.totalCPUTime, ",", p.maxIOBurst, ")")
        print("\tFinishing time: ", p.finishTime)
        print("\tTurnaround time: ", p.turnAroundTime)
        print("\tI/O time: ", p.IOtime)
        print("\tWaiting time: ", p.waitTime)
        totalRunTime += p.totalCPUTime
        avgTurnaround += p.turnAroundTime
        avgWaiting += p.waitTime

    print("Suymmary Data: ")
    print("\tFinishing time: ", finishTime)
    print("\tCPU Utilization: ", totalRunTime/finishTime)
    print("\tI/O Utilization: ", cycleContainBlock/finishTime)
    print("\tThroughput: ", (100 / finishTime * len(processes)), "processes per hundred cycles")
    print("\tAverage turnaround time: ", avgTurnaround/len(processes))
    print("\tAverage waiting time: ", avgWaiting/len(processes))



def Uniprogrammed():
    processes = []
    readyProcess = []
    processToRun = 0
    time = 0
    finished = False
    processCount = 0
    cycleContainBlock = 0
    global counter
    counter = 0
    for p in sortedInput:
        if len(p) > 0:
            processes.append(Process(p[0], p[1], p[2], p[3], processCount))
            processCount += 1

    while (finished == False):
        if isVerbose:
            print("Before cycle " + str(time) + ": ", end="")
        readyProcess.clear()
        for p in processes:
            if isVerbose:
                num = 0
                if p.status == "running":
                    num = p.CPUBurst
                elif p.status == "blocked":
                    num = p.remainingIOBurst
                print(p.status + " " + str(num) + " ", end="")
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
                    processToRun += 1
                    p.running = False
                    p.finishTime = time
                    p.turnAroundTime = time - p.arrivalTime
                elif p.CPUBurst <= 0:
                    p.status = "blocked"
                    p.remainingIOBurst = randomOS(p.maxIOBurst, counter)
                    counter += 1
                    p.running = False
                    p.blocked = True
            if p.status == "unstarted" and time >= int(p.arrivalTime):
                p.status = "ready"
            if p.status == "ready":
                readyProcess.append(p)

        processRunning = False
        for p in processes:
            if p.running:
                processRunning = True

        for p in processes:
            if p.blocked:
                cycleContainBlock += 1
                break

        # choose a process to run
        if not processRunning:
            if len(readyProcess) != 0:
                processRun = readyProcess.pop(0)
                for p in readyProcess:
                    if p.arrivalTime < processRun.arrivalTime:
                        processRun = p
                    elif p.arrivalTime == processRun.arrivalTime:
                        if p.processID < processRun.processID:
                            processRun = p

                # Increment waiting time for process not running
                for p in readyProcess:
                    if processRun != p:
                        p.curWaitTime += 1

                if processToRun == processRun.processNum:
                    # Run process
                    processRun.status = "running"
                    processRun.curWaitTime = 0
                    processRun.CPUBurst = randomOS(processRun.maxCPUBurst, counter)
                    counter += 1
                    processRun.running = True

        for p in processes:
            if p.status == "ready":
                p.waitTime += 1
            if p.status == "blocked":
                p.IOtime += 1

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
    print("The scheduling algorithm used was Uniprocessor")
    for p in processes:
        print("Process ", p.processNum, ":")
        print("\t(A, B, C, IO) = (", p.arrivalTime, ",", p.maxCPUBurst, ",", p.totalCPUTime, ",", p.maxIOBurst, ")")
        print("\tFinishing time: ", p.finishTime)
        print("\tTurnaround time: ", p.turnAroundTime)
        print("\tI/O time: ", p.IOtime)
        print("\tWaiting time: ", p.waitTime)
        totalRunTime += p.totalCPUTime
        avgTurnaround += p.turnAroundTime
        avgWaiting += p.waitTime

    print("Suymmary Data: ")
    print("\tFinishing time: ", finishTime)
    print("\tCPU Utilization: ", totalRunTime/finishTime)
    print("\tI/O Utilization: ", cycleContainBlock/finishTime)
    print("\tThroughput: ", (100 / finishTime * len(processes)), "processes per hundred cycles")
    print("\tAverage turnaround time: ", avgTurnaround/len(processes))
    print("\tAverage waiting time: ", avgWaiting/len(processes))


# Shortest execution time first
def SJF():
    processes = []
    readyProcess = []
    time = 0
    finished = False
    processCount = 0
    cycleContainBlock = 0
    global counter
    counter = 0
    for p in sortedInput:
        if len(p) > 0:
            processes.append(Process(p[0], p[1], p[2], p[3], processCount))
            processCount += 1

    while (finished == False):
        if isVerbose:
            print("Before cycle " + str(time) + ": ", end="")
        readyProcess.clear()
        for p in processes:
            if isVerbose:
                num = 0
                if p.status == "running":
                    num = p.CPUBurst
                elif p.status == "blocked":
                    num = p.remainingIOBurst
                print(p.status + " " + str(num) + " ", end="")
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
                    p.remainingIOBurst = randomOS(p.maxIOBurst, counter)
                    counter += 1
                    p.running = False
                    p.blocked = True
            if p.status == "unstarted" and time >= int(p.arrivalTime):
                p.status = "ready"
            if p.status == "ready":
                readyProcess.append(p)

        processRunning = False
        for p in processes:
            if p.running:
                processRunning = True

        for p in processes:
            if p.blocked:
                cycleContainBlock += 1
                break

        # choose a process to run
        if not processRunning:
            if len(readyProcess) != 0:
                processRun = readyProcess.pop(0)
                for p in readyProcess:
                    if p.remainingCPUTime < processRun.remainingCPUTime:
                        processRun = p

                # Increment waiting time for process not running
                for p in readyProcess:
                    if processRun != p:
                        p.curWaitTime += 1

                # Run process
                processRun.status = "running"
                processRun.curWaitTime = 0
                processRun.CPUBurst = randomOS(processRun.maxCPUBurst, counter)
                counter += 1
                processRun.running = True

        for p in processes:
            if p.status == "ready":
                p.waitTime += 1
            if p.status == "blocked":
                p.IOtime += 1

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
    print("The scheduling algorithm used was Shortest Job First")
    for p in processes:
        print("Process ", p.processNum, ":")
        print("\t(A, B, C, IO) = (", p.arrivalTime, ",", p.maxCPUBurst, ",", p.totalCPUTime, ",", p.maxIOBurst, ")")
        print("\tFinishing time: ", p.finishTime)
        print("\tTurnaround time: ", p.turnAroundTime)
        print("\tI/O time: ", p.IOtime)
        print("\tWaiting time: ", p.waitTime)
        totalRunTime += p.totalCPUTime
        avgTurnaround += p.turnAroundTime
        avgWaiting += p.waitTime

    print("Suymmary Data: ")
    print("\tFinishing time: ", finishTime)
    print("\tCPU Utilization: ", totalRunTime/finishTime)
    print("\tI/O Utilization: ", cycleContainBlock/finishTime)
    print("\tThroughput: ", (100 / finishTime * len(processes)), "processes per hundred cycles")
    print("\tAverage turnaround time: ", avgTurnaround/len(processes))
    print("\tAverage waiting time: ", avgWaiting/len(processes))


# FCFS()
RR()
# Uniprogrammed()
# SJF()
