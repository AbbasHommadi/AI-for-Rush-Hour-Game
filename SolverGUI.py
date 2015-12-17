#__author__ = 'Abbas'
import time
from tkinter import *
from AStar import ZeroHeuristic, DistanceFromTargetToExit, BlockingExitHeuristic, BlockingLowerBoundEstimation
from AStar import AStar
from LoadRushHourFile import load_file
from Vehicle import CAR_ID, TRUCK_ID

boardConfigsFolder = "C:/Users/Abbas/PycharmProjects/Rush Hour Puzzle Game/New folder"

class RushHourSolverApp:
    def __init__(self):
        self.root = Tk()
        height = 450
        width = 350
        self.frame = Frame(self.root, height = height, width = width)
        # self.frame.grid_propagate(False)
        self.frame.pack()

        # create menues
        menu = Menu(self.root)
        self.root.config(menu=menu)
        self.fileMenu = Menu(menu)
        menu.add_cascade(label="File", menu=self.fileMenu)
        self.fileMenu.add_command(label="Exit", command=self.root.quit)
        self.startingForm()
        self.root.mainloop()

    def startingForm(self):
        self.clearFrame()
        self.rushhour = None
        self.topPanel  = LabelFrame(self.frame, text='Select a puzzle',height = 50, width=350)
        self.topPanel.grid_propagate(False)
        self.topPanel.grid(row = 0, column = 0,columnspan=2,padx =5, pady=5,sticky=E+W)

        self.bottomLeftPanel = LabelFrame(self.frame, text='Rush Hour Puzzle', height = 400, width=350)
        self.bottomLeftPanel.grid_propagate(False)
        self.bottomLeftPanel.grid(row = 1,column=0,padx =5, pady=5, sticky=E+W)

        self.bottomRightPanel = LabelFrame(self.frame, text='Select a Heuristic',height = 400, width = 160)
        self.bottomRightPanel.grid_propagate(False)
        self.bottomRightPanel.grid(row = 1, column = 1, sticky=E+W,padx =5, pady=5)

        lbl = Label(self.topPanel, text = 'Choose # Vehicles:')
        lbl.grid(row = 1, column = 0)
        self.spinBoxNumOfVehicle = Spinbox(self.topPanel, width = 5, from_ = 4, to=15)
        self.spinBoxNumOfVehicle.grid(row= 1, column = 1, padx=10, pady=5)

        lbl = Label(self.topPanel, text = 'Choose a puzzle:')
        lbl.grid(row = 1, column = 2)
        self.spinBoxPuzzleNum = Spinbox(self.topPanel, width = 5, from_ = 1, to=25)
        self.spinBoxPuzzleNum.grid(row= 1, column = 3, padx=10, pady=5)

        self.heuristicChoice = IntVar()
        self.heuristicChoice.set(1)  # initializing the choice, i.e. H0
        self.choices = [("H0",1),("H1",2),("H2",3),("H3",4),]
        print(self.heuristicChoice.get())
        i=0
        for txt, val in self.choices:
            rbtn = Radiobutton(self.bottomRightPanel, text=txt,  variable=self.heuristicChoice,  value=val)
            rbtn.grid(row = i, column = 0, sticky=W)
            i+=1

        self.btnSolvePuzzle = Button(self.bottomRightPanel,text = 'Solve', width =15, command = self.solvePuzzle, bg='darkgray')
        self.btnSolvePuzzle.grid(columnspan=2,row=i,column=0, sticky=W,padx=2)

        self.lblSteps = Label(self.bottomRightPanel, text = '', fg='blue')
        self.lblSteps.grid(row = 7, column = 1,sticky=W)

        self.lblExpandedNodes = Label(self.bottomRightPanel, text = '',fg='blue')
        self.lblExpandedNodes.grid(row = 8, column = 1,sticky=W)

        self.lblrunningTime = Label(self.bottomRightPanel, text = '',fg='blue')
        self.lblrunningTime.grid(row = 9, column = 1,sticky=W)

        self.disablePanel(self.bottomRightPanel)
        self.disablePanel(self.bottomLeftPanel)

        self.btnSave = Button(self.topPanel,text = 'Save', width =15,bg='darkgray', command = self.LoadPuzzle)
        self.btnSave.grid(columnspan=2,row=1,column=4)

    def solvePuzzle(self):
        self.lblSteps['text']=''
        self.lblSteps.update()
        self.lblExpandedNodes['text']=''
        self.lblExpandedNodes.update()
        self.lblrunningTime['text']=''
        self.lblrunningTime.update()
        self.drawBoard(self.rushhour.get_board())

        heuristic = ZeroHeuristic()
        if self.heuristicChoice.get() == 2:
            heuristic = DistanceFromTargetToExit()
        elif self.heuristicChoice.get() == 3:
            heuristic = BlockingExitHeuristic()
        elif self.heuristicChoice.get() == 4:
            heuristic = BlockingLowerBoundEstimation()
        aStar = AStar(heuristic)
        elapsedTime = time.time()
        sol = aStar.aStar(self.rushhour)
        runningTime = round((time.time()-elapsedTime)*1000)
        lbl = Label(self.bottomRightPanel, text = 'Steps: ')
        lbl.grid(row = 7, column = 0,sticky=W)

        steps = 0
        for board in sol['Solution']:
            self.drawBoard(board.get_board())
            self.lblSteps['text'] = str(steps)
            self.lblSteps.update()
            steps += 1
            time.sleep(.5)
        lbl = Label(self.bottomRightPanel, text = 'Expanded Nodes: ')
        lbl.grid(row = 8, column = 0,sticky=W)

        lbl = Label(self.bottomRightPanel, text = 'Running Time: ')
        lbl.grid(row = 9, column = 0,sticky=W)

        self.lblExpandedNodes['text'] = str(sol['Expanded Nodes'])
        self.lblrunningTime['text'] = str(runningTime)+' ms'

    def LoadPuzzle(self):
        self.enablePanel(self.bottomRightPanel)
        self.lblSteps['text']=''
        self.lblSteps.update()
        self.lblExpandedNodes['text']=''
        self.lblExpandedNodes.update()
        self.lblrunningTime['text']=''
        self.lblrunningTime.update()
        filename =boardConfigsFolder+"/" +"{}_{}.txt".format(int(self.spinBoxNumOfVehicle.get())-1,int(self.spinBoxPuzzleNum.get())-1)
        print(filename)
        self.rushhour = load_file(filename)
        self.drawBoard(self.rushhour.get_board())

    def drawBoard(self, board):
        for widget in self.bottomLeftPanel.winfo_children():
            widget.destroy()
        for y in range(6):
            for x in range(6):
                color = 'lightgray'
                if board[y][x]=='X':
                    color = 'brown'
                elif board[y][x] in  CAR_ID:
                    color = 'orange'
                elif board[y][x] in  TRUCK_ID:
                    color = 'darkblue'
                lbl = Label(self.bottomLeftPanel, text = board[y][x], width =5,height=3, fg="white",bg=color, font='Times 12 bold')
                lbl.grid_propagate(False)
                lbl.grid(row = y+2, column = x+3, padx=1,pady=1,sticky=E+W )
        lbl = Label(self.bottomLeftPanel, text = 'Exit', width =2,height=3, fg="white",bg='darkGreen', font='Times 12 bold')
        lbl.grid_propagate(False)
        lbl.grid(row = 4, column = 9, padx=1,pady=1,sticky=E+W )
        self.bottomLeftPanel.update()

    def disablePanel(self,panel):
        for widget in panel.winfo_children():
            widget.config(state= DISABLED)

    def enablePanel(self,panel):
        for widget in panel.winfo_children():
            widget.config(state= NORMAL)

    def clearFrame(self):
        '''
        This method destroy all widgets inside the form
        '''
        for widget in self.frame.winfo_children():
            widget.destroy()

if __name__=='__main__':
    rushHourSolverApp = RushHourSolverApp()