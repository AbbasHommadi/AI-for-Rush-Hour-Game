from Vehicle import Vehicle
import copy
GOAL_VEHICLE = Vehicle('X', 4, 2,'H')
class RushHour(object):

    def __init__(self, vehicles, depth = 0, hvalue = 0):
        self.vehicles = vehicles
        self.depth = depth
        self.hvalue = hvalue

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return self.vehicles == other.vehicles

    def __cmp__(self, b):
        if self.hvalue+self.depth==b.hvalue+b.depth:
            return 0
        else:
            if self.depth + self.hvalue>b.depth+ b.hvalue:
                return 1
            return -1

    def __lt__(self, other):
            return self.depth + self.hvalue < other.depth + other.hvalue

    def __gt__(self, other):
        return self.depth + self.hvalue > other.depth + other.hvalue

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        s = '~' * 8 + '\n'
        for line in self.get_board():
            s += '|{0}|\n'.format(''.join(line))
        s += '~' * 8 + '\n'
        return s

    def get_board(self):
        board = [[' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' ']]
        for vehicle in self.vehicles:
            x = vehicle.x
            y = vehicle.y
            if vehicle.vehicleType == 'H':
                for i in range(0,vehicle.size):
                    board[y][x+i] = vehicle.id
            else:# the vehicle is vertical
                for i in range(vehicle.size):
                    board[y+i][x] = vehicle.id
        return board

    def getNextPossibleMoves(self):
        board = self.get_board()
        for vehicle in self.vehicles:
            if vehicle.vehicleType == 'H':
                if vehicle.x - 1 >= 0 and board[vehicle.y][vehicle.x - 1] == ' ':   # check left position
                    new_vehicle = Vehicle(vehicle.id, vehicle.x - 1, vehicle.y, vehicle.vehicleType)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(vehicle)
                    new_vehicles.add(new_vehicle)
                    yield RushHour(new_vehicles)
                if vehicle.x + vehicle.size <= 5 and board[vehicle.y][vehicle.x + vehicle.size] == ' ': #check right position
                    new_vehicle = Vehicle(vehicle.id, vehicle.x + 1, vehicle.y, vehicle.vehicleType)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(vehicle)
                    new_vehicles.add(new_vehicle)
                    yield RushHour(new_vehicles)
            else: # for vertical vehicles
                if vehicle.y - 1 >= 0 and board[vehicle.y - 1][vehicle.x] == ' ': # check up position
                    new_vehicle = Vehicle(vehicle.id, vehicle.x, vehicle.y - 1, vehicle.vehicleType)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(vehicle)
                    new_vehicles.add(new_vehicle)
                    yield RushHour(new_vehicles)
                if vehicle.y + vehicle.size <= 5 and board[vehicle.y + vehicle.size][vehicle.x] == ' ': # check bottom position
                    new_vehicle = Vehicle(vehicle.id, vehicle.x, vehicle.y + 1, vehicle.vehicleType)
                    new_vehicles = self.vehicles.copy()
                    new_vehicles.remove(vehicle)
                    new_vehicles.add(new_vehicle)
                    yield RushHour(new_vehicles)

    def moveVehicle(self,id, direction, distance):
        for vehicle in self.vehicles:
            if vehicle.id and id:
                vehicle.move(direction, distance)
                break
    def isSolved(self):
        return GOAL_VEHICLE in self.vehicles

    def isSamePuzzle(self,otherRushHour):
        if len(self.vehicles) == len(otherRushHour.vehicles):
            countSameVehicles = 0
            for vehicle1 in self.vehicles:
                for vehicle2 in otherRushHour.vehicles:
                    if vehicle1.size == vehicle2.size and vehicle1.vehicleType == vehicle2.vehicleType and vehicle1.x == vehicle2.x and vehicle1.y == vehicle2.y:
                        countSameVehicles +=1
                        break
            if countSameVehicles == len(self.vehicles):
                return True
        return False

    def getTragetVehicle(self):
        for v in self.vehicles:
            if v.id =='X':
                return v
        return None




