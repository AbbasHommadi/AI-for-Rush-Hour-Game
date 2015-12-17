#__author__ = 'Abbas'
import csv
from AStar import *
from LoadRushHourFile import load_file, savePuzzle


class GenerateHarderPuzzle:
    '''
    This class implement Hill climbing to generate harder puzzle for a given one
    '''
    def hillClimbing(self, puzzle):
        '''
        This method take an puzzle and generate a harder puzzle (the steps required to solve should be greater than the already generated puzzle)
        by applying hill climbing technique
        :param puzzle: the puzzle that will be used to generate a harder puzzle
        :return: Same puzzle if there is no harder puzzle otherwise a new puzzle which is harder than already known puzzle
        '''
        h = ZeroHeuristic()
        aStar = AStar(h)
        currentPuzzle = puzzle
        sol = aStar.aStar(currentPuzzle)
        currentEval = sol['Steps']
        print( 'Input Steps',currentEval, end="")
        while True:
            nextPuzzle = None
            nextPuzzleEval = -1000
            for neighbor in currentPuzzle.getNextPossibleMoves():
                sol = aStar.aStar(neighbor)
                if sol['Steps'] > nextPuzzleEval:
                    nextPuzzleEval = sol['Steps']
                    nextPuzzle = RushHour(set(neighbor.vehicles))
            if nextPuzzleEval <= currentEval:
                print(' Out Steps',currentEval)
                return currentPuzzle
            currentPuzzle = RushHour(set(nextPuzzle.vehicles))
            currentEval = nextPuzzleEval

boardConfigsFolder = "C:/Users/Abbas/PycharmProjects/Rush Hour Puzzle Game/New folder"
harderPuzzlesFolder = "C:/Users/Abbas/PycharmProjects/Rush Hour Puzzle Game/HarderPuzzles"
generateHarderPuzzle = GenerateHarderPuzzle()


def recordHillClimbing():
    data = []
    h0 = ZeroHeuristic()
    aStarWithH0 = AStar(h0)
    for i in range(0, 15):
        for j in range(0, 25):
            filename = '{0}_{1}.txt'.format(i, j)
            r = load_file(boardConfigsFolder + '/{0}'.format(filename))
            sol1 = aStarWithH0.aStar(r)
            rr = load_file(harderPuzzlesFolder + '/{0}'.format(filename))
            sol2 = aStarWithH0.aStar(rr)
            data.append([filename, sol1['Steps'], sol2['Steps']])
            print(filename,sol1['Steps'], sol2['Steps'])
    with open('hillClimbing.csv', 'w', newline='') as f:
        wr = csv.writer(f, delimiter=',')
        wr.writerows(data)


if __name__ == '__main__':
    for i in range(13,15):
        for j in range(0,25):
            filename = '{0}_{1}.txt'.format(i,j)
            print('puzzle file {0}'.format(filename))
            puzzle = load_file(boardConfigsFolder+'/{0}'.format(filename))
            harderPuzzle = generateHarderPuzzle.hillClimbing(puzzle)
            savePuzzle(harderPuzzle, harderPuzzlesFolder+'/'+filename)
    recordHillClimbing()