#!/usr/bin/env python3


#Jerdon Helgeson
#11-12-18
#CPTS 481 HW6 Game of life

from tkinter import Tk
from tkinter import Frame
from tkinter import Button
from tkinter import *
import time


class Cell():
    def __init__(self, alive = 0):
        self.alive = alive
        self.aliveNeighbors = 0
    def update(self):
        #self.aliveNeighbors = aliveNeighbors
        if(self.aliveNeighbors == 3 or self.aliveNeighbors == 2):
            if(self.alive == 0 and self.aliveNeighbors == 3):
                self.alive = 1
                return 1
            else:
                return -1
        else:
            if(self.alive == 1):
                self.alive = 0
                return 0
            else:
                return -1
            

    def __eq__(self,other):
        if(isinstance(other, Cell)):
            return self.alive == other.alive
        else:
            return self.alive == other

    def __str__(self):
        return str(self.alive)
    def __repr__(self):
        return str(self.alive)
        
        

class CellArray():
    def __init__(self):
        self.l = [[Cell(0) for i in range(20)] for x in range(20)]

    def checkLoc(self,loc = (0,0)):
        if(self.l[loc[0]][loc[1]] == 1):
            return True
        else:
            return False

    def clear(self):
        self.l = [[Cell(0) for i in range(20)] for x in range(20)]

    def click(self, loc = (0,0)):
        if((self.l)[loc[0]][loc[1]] == 0):
            (self.l)[loc[0]][loc[1]].alive = 1
            self.tellNeighbors(loc, 1)
        else:
            (self.l)[loc[0]][loc[1]].alive = 0
            self.tellNeighbors(loc, 0)

    def tellNeighbors(self, loc = (0,0), alive = 1):
        """this will update all neighbors and their aliveNeighbors status"""
        live = alive
        if(alive == 0):
            live = -1
        if((loc[0] > 0 and loc[0] < 19)and(loc[1] > 0 and loc[1] < 19)):
            #this cell has all 8 neighbors
            (self.l)[loc[0]-1][loc[1]-1].aliveNeighbors += live
            (self.l)[loc[0]-1][loc[1]].aliveNeighbors += live
            (self.l)[loc[0]-1][loc[1]+1].aliveNeighbors += live
            (self.l)[loc[0]][loc[1] - 1].aliveNeighbors += live
            (self.l)[loc[0]][loc[1] + 1].aliveNeighbors += live
            (self.l)[loc[0]+1][loc[1]-1].aliveNeighbors += live
            (self.l)[loc[0]+1][loc[1]].aliveNeighbors += live
            (self.l)[loc[0]+1][loc[1]+1].aliveNeighbors += live    
        elif(loc[0] == 0):
            if(loc[1] == 0):
                #corner (top-left)      - 3 neighbors
                (self.l)[loc[0]][loc[1]+1].aliveNeighbors += live
                (self.l)[loc[0]+1][loc[1]+1].aliveNeighbors += live
                (self.l)[loc[0]+1][loc[1]].aliveNeighbors += live
            elif(loc[1] == 19):
                #corner (top-right)     - 3 neighbors
                (self.l)[loc[0]][loc[1]-1].aliveNeighbors += live
                (self.l)[loc[0]+1][loc[1]-1].aliveNeighbors += live
                (self.l)[loc[0]+1][loc[1]].aliveNeighbors += live
            else:
                #edge   (top)           - 5 neighbors
                (self.l)[loc[0]][loc[1]-1].aliveNeighbors += live
                (self.l)[loc[0]][loc[1]+1].aliveNeighbors += live
                (self.l)[loc[0]+1][loc[1]].aliveNeighbors += live
                (self.l)[loc[0]+1][loc[1]-1].aliveNeighbors += live
                (self.l)[loc[0]+1][loc[1]+1].aliveNeighbors += live
        elif(loc[0] == 19):
            if(loc[1] == 0):
                #corner (bottom-left)   - 3 neighbors
                (self.l)[loc[0]-1][loc[1]].aliveNeighbors += live
                (self.l)[loc[0]-1][loc[1]+1].aliveNeighbors += live
                (self.l)[loc[0]][loc[1]+1].aliveNeighbors += live
            elif(loc[1] == 19):
                #corner (bottom-right)  - 3 neighbors
                (self.l)[loc[0]][loc[1]-1].aliveNeighbors += live
                (self.l)[loc[0]-1][loc[1]-1].aliveNeighbors += live
                (self.l)[loc[0]-1][loc[1]].aliveNeighbors += live
            else:
                #edge   (bottom)        - 5 neighbors
                (self.l)[loc[0]][loc[1]-1].aliveNeighbors += live
                (self.l)[loc[0]][loc[1]+1].aliveNeighbors += live
                (self.l)[loc[0]-1][loc[1]].aliveNeighbors += live
                (self.l)[loc[0]-1][loc[1]-1].aliveNeighbors += live
                (self.l)[loc[0]-1][loc[1]+1].aliveNeighbors += live
        elif(loc[1] == 0):
            #    edge   (left)          - 5 neighbors
            (self.l)[loc[0]+1][loc[1]+1].aliveNeighbors += live
            (self.l)[loc[0]-1][loc[1]+1].aliveNeighbors += live
            (self.l)[loc[0]][loc[1]+1].aliveNeighbors += live
            (self.l)[loc[0]-1][loc[1]].aliveNeighbors += live
            (self.l)[loc[0]+1][loc[1]].aliveNeighbors += live
        elif(loc[1] == 19):
            #    edge   (right)         - 5 neighbors
            (self.l)[loc[0]+1][loc[1]-1].aliveNeighbors += live
            (self.l)[loc[0]-1][loc[1]-1].aliveNeighbors += live
            (self.l)[loc[0]][loc[1]-1].aliveNeighbors += live
            (self.l)[loc[0]-1][loc[1]].aliveNeighbors += live
            (self.l)[loc[0]+1][loc[1]].aliveNeighbors += live
            
                

    def step(self):
        r = 0
        c = 0
        statusRecord = [[None for i in range(20)] for x in range(20)]
        for row in self.l:
            c = 0
            for cell in row:
                status = cell.update()
                statusRecord[r][c] = status
                c += 1
            r+=1
        r = 0
        c = 0
        for row in self.l:
            c = 0
            for cell in row:
                if(statusRecord[r][c] != -1):
                    self.tellNeighbors((r,c),statusRecord[r][c])
                c+=1
            r+=1
        

    def __str__(self):
        lStr = "ALIVE BOARD\t\t\t\t\tNEIGHBORS BOARD \n"
        for i in self.l:
            lStr += "["
            for c in i:
                lStr += str(c.alive)
                lStr += ","
            lStr = lStr[:-1]
            lStr += "]\t["
            for c in i:
                lStr += str(c.aliveNeighbors)
                lStr += ","
            lStr = lStr[:-1]
            lStr += "]\n"
        return lStr
                
                
    def __repr__(self):
        lStr = ""
        #if(neighbors == False):
        for i in self.l:
            lStr += "["
            for c in i:
                lStr += ","
                lStr += str(c.alive)
            lStr = lStr[:-1]
            lStr += "]\n"            
        return lStr

    def showNeighbors(self):
        lStr = ""
        for i in self.l:
            lStr += "["
            for c in i:
                lStr += ","
                lStr += str(c.aliveNeighbors)
            lStr = lStr[:-1]
            lStr += "]\n"
        print(lStr)

def click(event):
    w = canvas.winfo_width()/20
    h = canvas.winfo_height()/20
    col = int(event.x//w)
    row = int(event.y//h)
    cA.click((row,col))
    print(cA)
    if(cA.checkLoc((row,col))):
        colorRecord[row][col]  = canvas.create_rectangle(col*w, row*h, (col+1)*w, (row+1)*h, fill="black")
    else:
        canvas.delete(colorRecord[row][col])
        colorRecord[row][col] = None
        
    #print("row: ", row, "  col: ", col )
def stepM():
    print("STEP")
    cA.step()
    print(cA)
    colorBoard()

def colorBoard():
    #print("******************COLOR BOARD*****************")
    row = 0
    col = 0
    w = canvas.winfo_width()/20
    h = canvas.winfo_height()/20
    for r in cA.l:
        col = 0
        for c in r:
            if(c.alive == 0):
                if(colorRecord[row][col] != None):
                    canvas.delete(colorRecord[row][col])
                    colorRecord[row][col] = None
            else:
                if(colorRecord[row][col] == None):
                    colorRecord[row][col]  = canvas.create_rectangle(col*w, row*h, (col+1)*w, (row+1)*h, fill="black")
            col += 1
        row += 1
    
def clear():
    cA.clear()
    colorBoard()
    print(cA)

def byebye():
    quit()

def runM():
    stepM()
    canvas.update_idletasks()
    root.after(1000,runM)
    
    
        
    
#if __name__ == "__main__":
cA = CellArray()
colorRecord = [[None for i in range(20)] for x in range(20)]
root = Tk()
root.title("The Game of Life")
frame = Frame(root, width=500, height=500)
frame.pack()
canvas = Canvas(frame, width=500, height=500, bd = 5)
canvas.pack()
canvas.bind("<Button-1>", click)

step = Button(root, text="Step", command=stepM)
step.pack(side = LEFT, padx = 40)
clear = Button(root, text="Clear", command=clear)
clear.pack(side = LEFT, padx = 40)
run = Button(root, text="Run", command=runM)
run.pack(side = LEFT, padx = 40)
clear = Button(root, text="Quit", command=byebye)
clear.pack(side = LEFT, padx = 40)
5
