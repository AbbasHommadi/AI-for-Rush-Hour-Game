#__author__ = 'Abbas'
import random
from AStar import AStar, ZeroHeuristic, BlockingExitHeuristic
from LoadRushHourFile import savePuzzle
from RushHour import *
from Vehicle import *
CAR_ID = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K')
TRUCK_ID = ('O', 'P', 'Q', 'R','S','T','U','V','W','Y','Z')
vehicleType=['H', 'V']
class Generator(object):
    '''
    This class generates random puzzle configuration for rush hour game
    '''
    def __init__(self, minNumOfVehicles, maxNumOfVehicles):
        self.numVehiclesRange = [minNumOfVehicles, maxNumOfVehicles]

    def generate(self):
        '''
        Generate random puzzle where number of vehicles in range min and max that are specified already
        :return: RushHour Object where the configuration created randomly
        '''
        numOfVehicles = random.randint(self.numVehiclesRange[0],self.numVehiclesRange[1])
        x = random.randint(0,3)
        y = 2
        carIDIndex = 0
        truckIDIndex = 0
        self.targetVehicle = Vehicle('X',x, y,vehicleType[0])
        vehicles = [self.targetVehicle]

        for i in range(0,numOfVehicles):
            randomVehicle = self.__getRandomVehicle(carIDIndex,truckIDIndex)
            attempts = 0
            while True:
                alreadyExist = False
                for vehicle in vehicles:
                    if vehicle.crash(randomVehicle) or (randomVehicle.vehicleType =='H' and randomVehicle.y == 2 and randomVehicle.x > self.targetVehicle.x):
                        alreadyExist = True
                        break
                if alreadyExist:
                    randomVehicle = self.__getRandomVehicle(carIDIndex,truckIDIndex)
                    attempts+=1
                else:
                    break
                if attempts>200:
                    return None
            vehicles.append(randomVehicle)
            if(randomVehicle.size==2):
                carIDIndex+=1
                if carIDIndex>= len(CAR_ID):
                    carIDIndex = 0
            else:
                truckIDIndex+=1
                if truckIDIndex>= len(TRUCK_ID):
                    truckIDIndex = 0
        return RushHour(set(vehicles))

    def __onBoundries(self, x, y, size, vehicleType):
        '''
        This method check the vehicle is in boundary of the board or not
        :param x: x coordinate
        :param y: y coordinate
        :param size: size of vehicle which either 2 or 3
        :param vehicleType: vehicle type which is either H or V
        :return: True if the vehicle on boundries Fals otherwise
        '''
        if (x < 0 | x > 5 | y < 0 | y >5):
            return False
        if (vehicleType =='H' and x+size > 5) | (vehicleType =='V' and y+size > 5):
            return False
        return True

    def __getRandomVehicle(self,carIDIndex, truckIDIndex):
        '''
        This method create random vehicle by randomize x and y, type H or V, and car or truck
        :param carIDIndex: car index for car list
        :param truckIDIndex: truck index for truck list
        :return: Vehicle object with random position and type
        '''
        randomVType = vehicleType[random.randint(0,1)]
        randomSize = random.randint(2,3)
        if randomSize==3 :#and truckIDIndex < 4 :
            randomVehicleID = TRUCK_ID[truckIDIndex]
        else :
            randomVehicleID = CAR_ID[carIDIndex]
            randomSize = 2

        x = random.randint(0,5)
        y = random.randint(0,5)
        while not self.__onBoundries(x, y, randomSize, randomVType) :
            x = random.randint(0,5)
            y = random.randint(0,5)
        return Vehicle(randomVehicleID,x,y,randomVType)

##########################
boardConfigsFolder = "C:/Users/Abbas/PycharmProjects/Rush Hour Puzzle Game/New folder"
if __name__ == '__main__':
    aStar = AStar(BlockingExitHeuristic())
    rushHourPuzzles = []
    generator = Generator(12,12)
    i = 0
    while i < 25:
        puzzle = generator.generate()
        if puzzle:
            sol = aStar.aStar(puzzle)
            if sol['Steps'] > 10 :
                while True:
                    alreadyExist = False
                    for p in rushHourPuzzles:
                        if p.isSamePuzzle(puzzle):
                            alreadyExist = True
                            break
                    if not alreadyExist:
                        break
                    puzzle = generator.generate()

                rushHourPuzzles.append(puzzle)
                filename =boardConfigsFolder+"/" +"12_{0}.txt".format(i)
                savePuzzle(puzzle, filename)
                print("Puzzle {0}".format(i), "Steps {0}".format(sol['Steps']))
                i +=1

