CAR_ID = ('X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K')
TRUCK_ID = ('O', 'P', 'Q', 'R','S','T','U','V','W','Y','Z')

class Vehicle(object):
    def __init__(self, id, x, y, vehicleType):
        self.id = id
        if id in CAR_ID:
            self.size = 2
        elif id in TRUCK_ID:
            self.size = 3
        else:
            raise ValueError('Invalid id {0}'.format(id))
        # checking the coordination of a vehicle
        if 0 <= x <= 5:
            self.x = x
        else:
            raise ValueError('Invalid x {0}'.format(x))

        if 0 <= y <= 5:
            self.y = y
        else:
            raise ValueError('Invalid y {0}'.format(y))

        self.vehicleType = vehicleType
        if vehicleType == 'H': # Horizontal vehicle
            xEnd = self.x + (self.size - 1)
            yEnd = self.y
        elif vehicleType == 'V':
            xEnd = self.x
            yEnd = self.y + (self.size - 1)
        else:
            raise ValueError('Invalid vehicle type {0} It should be \'H\' or \'V\''.format(vehicleType))

        if xEnd > 5 or yEnd > 5:
            print(self.id,xEnd,yEnd)
            raise ValueError('Invalid configuration')

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self):
        return "Vehicle({0}, {1}, {2}, {3})".format(self.id, self.x, self.y,self.vehicleType)

    def crash(self,otherVehicle):
        if (otherVehicle.vehicleType=='H'):
            if(self.vehicleType=='H'):
                if (otherVehicle.y == self.y and ((otherVehicle.x>= self.x and otherVehicle.x < self.x+self.size)|(self.x >= otherVehicle.x and self.x< otherVehicle.x+otherVehicle.size))):
                    return True
            elif(self.vehicleType=='V'):
                if (otherVehicle.y >= self.y and otherVehicle.y < self.y+self.size and self.x >= otherVehicle.x and self.x < otherVehicle.x+otherVehicle.size):
                    return True
        elif (otherVehicle.vehicleType=='V'):
            if(self.vehicleType=='H'):
                if (otherVehicle.x>= self.x and otherVehicle.x < self.x+self.size and self.y>= otherVehicle.y and self.y < otherVehicle.y+otherVehicle.size):
                    return True
            elif(self.vehicleType=='V'):
                if (otherVehicle.x == self.x and ((otherVehicle.y >= self.y and otherVehicle.y < self.y+self.size) | (self.y >= otherVehicle.y and self.y < otherVehicle.y+otherVehicle.size))):
                    return True
        return False

    def move(self, direction, distance):
        if self.vehicleType == 'H' and (direction == 'UP' | direction == 'DOWN'):
            return False
        if self.vehicleType == 'V' and (direction == 'LEFT' | direction == 'RIGHT'):
            return False
        self.x
