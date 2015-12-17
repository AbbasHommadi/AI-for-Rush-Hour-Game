#__author__ = 'Abbas'
from AStar import *
from LoadRushHourFile import load_file
from main import breadth_first_search
import csv

boardConfigsFolder = "C:/Users/Abbas/PycharmProjects/Rush Hour Puzzle Game/New folder"
def saveResultIntoCSV(data, fileName):
    with open(fileName, 'w', newline='') as f:
        wr = csv.writer(f, delimiter=',')
        wr.writerows(data)
print('File#','Num of Vehicles','Heuristic','Time', 'Expanded Nodes', 'Steps', 'Solveable or not')
h0 = ZeroHeuristic()
h1 = DistanceFromTargetToExit()
h2 = BlockingExitHeuristic()
h3 = BlockingLowerBoundEstimation()
aStarWithH0 = AStar(h0)
aStarWithH1 = AStar(h1)
aStarWithH2 = AStar(h2)
aStarWithH3 = AStar(h3)
data = []
for i in range(3,15):
    for j in range(25):
        puzzleFile = boardConfigsFolder+"/" +"{0}_{1}.txt".format(i,j)
        rushHour = load_file(puzzleFile)
        elapsedTime = time.time()
        sol0 = aStarWithH0.aStar(rushHour)
        t0 = round((time.time()-elapsedTime)*1000)
        numVehicles = len(rushHour.vehicles)

        # data.append([i,numVehicles,'h0',t,sol['Expanded Nodes'],sol['Steps'],s])
        # print(i,numVehicles,'h0',t,sol['Expanded Nodes'],sol['Steps'],s)

        elapsedTime = time.time()
        sol1 = aStarWithH1.aStar(rushHour)
        t1 = round((time.time()-elapsedTime)*1000)

        # data.append([i,numVehicles,'h1',t,sol['Expanded Nodes'],sol['Steps'],s])
        # print(i,numVehicles,'h1',t,sol['Expanded Nodes'],sol['Steps'],s)

        elapsedTime = time.time()
        sol2 = aStarWithH2.aStar(rushHour)
        t2 = round((time.time()-elapsedTime)*1000)

        elapsedTime = time.time()
        sol3 = aStarWithH3.aStar(rushHour)
        t3 = round((time.time()-elapsedTime)*1000)
        data.append(["{0}_{1}.txt".format(i,j),numVehicles,'h0',t0,sol0['Expanded Nodes'],sol0['Steps'],'h1',t1,sol1['Expanded Nodes'],sol1['Steps'],'h2',t2,sol2['Expanded Nodes'],sol2['Steps'],'h3',t3,sol3['Expanded Nodes'],sol3['Steps']])
        print("{0}_{1}.txt".format(i,j),numVehicles,'h0',t0,sol0['Expanded Nodes'],sol0['Steps'],'h1',t1,sol1['Expanded Nodes'],sol1['Steps'],'h2',t2,sol2['Expanded Nodes'],sol2['Steps'],'h3',t3,sol3['Expanded Nodes'],sol3['Steps'])
saveResultIntoCSV(data, 'confStatistics_Dec13_.csv')