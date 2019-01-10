# ! / usr / bin / env python3


#Jerdon Helgeson
#11376111
#11-26-18
#HW7
#spreadsheet


from tkinter import Tk
from tkinter import Frame
from tkinter import Button
from tkinter import *
from math import *

class Cell():
    def __init__(self, row = 0, col = 0, eq = None, code = None ,value = None):
        self.row = row
        self.col = col
        self.expression = eq
        self.code = code
        self.value = value

    def __str__(self):
        return "Cell ("+ str(self.row)+ ","+ str(self.col)+"):" + str(self.value)
    def __repr__(self):
        return "Cell ("+ str(self.row)+ ","+ str(self.col)+"):" + str(self.value)
        

class Spreadsheet(Frame):
    def __init__(self, master = None,nr = 0, nc = 0):
        Frame.__init__(self,master)
        self.master = master
        self.master.bind("<Return>",self.setCell)
        self.nRows = nr #number of rows
        self.nCols = nc #number of columns
        y = self.nRows*22+52
        x = self.nCols*76+31
        geo = (str(x)+"x"+str(y))
        master.geometry(geo)
        master.configure(bg='grey')
        self.cells2D = [[Cell(r,c) for c in range(nc)] for r in range(nr)]
        self.symtab = {}
        self.cascaDe = {}
        self.focus = ("a",1)
        self.daBoard = Frame(self)
        self.daBoard.pack(side='top')
        self.daFocus = Frame(self)
        self.daFocus.pack(side='bottom')
        self.daFocus.focus_set()
        #self.pack()
        self.buildtkLabels()
        self.buildtkCells()
        self.buildFocus()
        

    def buildtkLabels(self):
        gridzero = Label(self.daBoard)
        gridzero.grid(row=0, column=0)
        for i in range(self.nCols):
            colNum = Label(self.daBoard,text=str(i), borderwidth = 1, relief = "solid", width = 8)
            colNum.grid(row=0, column=i+1)
        for r in range(self.nRows):
            rowLet = Label(self.daBoard, text=chr(ord('A')+r), borderwidth = 1, relief = "solid", width = 3)
            rowLet.grid(row=r+1, column=0)

    def buildtkCells(self):
        for c in range(self.nCols):
            for r in range(self.nRows):
                tcell = Label(self.daBoard, borderwidth = 1, relief = "solid", width = 8)
                tcell.grid(row=r+1, column=c+1)
                tcell.bind("<Button-1>",lambda event,rl = r, cl = c:
                           self.setFocus(coords = (rl,cl)))
                        
    def buildFocus(self, coords = None, error = None):
        if(error != None):
            self.focusLabel = Label(self.daFocus,text=self.focus[0]+str(self.focus[1])+":",
                                    borderwidth = 0, relief = "solid", width = 5)
            self.focusLabel.grid(row=0,column=0)
            self.focusEntry = Entry(self.daFocus, width = 16)
            self.focusEntry.insert(END, str(error))
            self.focusEntry.grid(row = 0, column = 1)
            
        elif(coords == None):
            self.focusLabel = Label(self.daFocus,text=self.focus[0]+str(self.focus[1])+":",
                                    borderwidth = 0, relief = "solid", width = 5)
            self.focusLabel.grid(row=0,column=0)
            cell = self.getCell((self.focus[0],self.focus[1]))
            #print("get cell: ",cell)            
            self.focusEntry = Entry(self.daFocus, width = 16)
            self.focusEntry.insert(END, str(cell.expression))
            self.focusEntry.grid(row = 0, column = 1)

        else:
            r = coords[0]
            c = coords[1]
            if(isinstance(r,str) == True):
                r = ord(r) - ord('a')
            self.focusLabel = Label(self.daFocus,text=self.focus[0]+str(self.focus[1])+":",
                                    borderwidth = 0, relief = "solid", width = 2)
            self.focusLabel.grid(row=0,column=0)
            cell = self.getCell((self.focus[0],self.focus[1]))
            self.focusEntry = Label(self.daFocus,text=str(cell.value),
                                    borderwidth = 0, relief = "solid",
                                    width = 16)
            self.focusEntry.grid(row = 0, column = 1)
            
        

    def getCell(self, event = None, coords = None):
        if(coords == None):
            r = self.focus[0]
            c = self.focus[1]
        else:
            r = coords[0]
            c = coords[1]
        if(isinstance(r,str) == True):
            r = ord(r) - ord('a')
        cell = self.cells2D[r][int(c)]
        return cell

    def setCell(self, event = None, coords = None, expr = None):
        if(coords == None):
            coords = (self.focus[0],self.focus[1])
        if(expr == None):
            expr = self.focusEntry.get()
            #print(str(coords[0])+str(coords[1])+": "+str(expr))
        r = coords[0]
        c = coords[1]
        if(isinstance(r,str) == True):
            r = ord(r) - ord('a')
        try:
            self.cells2D[r][c].expression = expr
            self.evaluate((r,c))
            self.cascade((r,c))
            self.setLabel(frame = self.daBoard, row = r, col = c)
            self.updateSymTab(row = r,col = c)
            print(self)
        except RecursionError:
            self.setFocus(error = "Error: Cyclic Dependancy")
            print("Cyclic Dependancy")

    def evaluate(self, coords = None):
        if(coords == None):
            coords = (self.focus[0],self.focus[1])
        r = coords[0]
        c = coords[1]
        try:
            self.cells2D[r][c].value = eval(str(self.cells2D[r][c].expression))
            self.updateSymTab(r,c,self.cells2D[r][c].value)
            #print("eval r:",r,", c: ",c,"*****TRY", self.cells2D[r][c].value)
        except:
            doSymEval = False
            for sym in self.symtab:
                if(sym in self.cells2D[r][c].expression):
                    doSymEval = True
                    self.cells2D[r][c].value = self.symEvaluate(self.cells2D[r][c].expression,row = r,col = c)
                    symCell = self.getCell(sym)
                    """print("symEval r:",r,", c: ",c,"*****symEval*****:",
                          self.cells2D[r][c].expression," ",self.cells2D[r][c].value,
                          "\nSym value: ",symCell.value)"""
            if(doSymEval == False):
                #it's just a string or it has incorrect notation so save as string
                self.cells2D[r][c].value = self.cells2D[r][c].expression
                #print("FailedSymEval r:",r,", c: ",c,"*****FailedSymEval", self.cells2D[r][c].value)

    def symEvaluate(self, expr,row = None, col = None):
        for s in self.symtab:
            if(s in expr):
                if(s in self.cascaDe):
                    csym = str(row)+str(col)
                    if(isinstance(row,int)):
                        cr = chr(row+97)
                        csym = str(cr)+str(col)
                    self.cascaDe[s].add(csym)
                else:
                    self.addToCascadeDict(s,row,col)
                expr = expr.replace(s, str(self.symtab[s]))
                #print("CascaDe: ", self.cascaDe)
        try:
            rExpr = eval(expr)
            #print("SYM EVAL: ",rExpr,",  Expr: ",expr)
            return rExpr
        except:
            return expr
                
        
        
    def setLabel(self, frame = None, row = None, col = None):
        if(frame == None):
            frame = self.daBoard
        if(row == None):
            row = self.focus[0]
        if(col == None):
            col = self.focus[1]
        for child in frame.children.values():
            info = child.grid_info()
            #print(info)
            if(info['row'] - 1 == int(row) and info['column'] - 1 == int(col)):
                child.config(text=str(self.cells2D[row][col].value))
                
            

    def setFocus(self,event = None, coords = None, error = None):
        if(error != None):
            self.buildFocus(error = error)
        else:
            r = coords[0]
            c = coords[1]
            if(isinstance(r,int) == True):
                r = chr(r+97)
            self.focus = (r,c)
            self.buildFocus()

    def updateSymTab(self,row = None, col = None, value = None):
        if(row == None):
            row = self.focus[0]
        if(col == None):
            col = self.focus[1]
        if(isinstance(row,int) == True):
            row = chr(row+97)
        sym = str(row)+str(col)
        if(value == None):
            cell = self.getCell((row,col))
            self.symtab[sym] = cell.value
            #print("cell Value:",cell.value)
            #print("symTab: ",self.symtab)
        else:
            self.symtab[sym] = value

    def isSym(self, sym):
        if(sym in self.symtab):
            return True
        return False

    def getSym(self, sym = None):
        if(isinstance(sym,tuple)):
            if(isinstance(sym[0]),int):
                r = chr(sym[0]+97)
            sym = str(r)+str(sym[1])
        elif(sym == None):
            sym = str(self.focus[0])+str(self.focus[1])
        return self.symtab[sym]
            
    def addToCascadeDict(self,sym,row,col):
        if(isinstance((sym[0]),int)):
            sr = chr(sym[0]+97)
            sym = str(sr)+str(sym[1:])
        if(isinstance(row,int)):
            cr = chr(row+97)
        csym = str(cr)+str(col)
        self.cascaDe[sym] = {csym}

    def cascade(self,coords):
        #print("COUNTING CASCADES")
        cr = coords[0]
        cDe = coords
        if(isinstance(coords,tuple)):
            if(isinstance(coords[0],int)):
                cr = chr(coords[0]+97)
            cDe = str(cr)+str(coords[1])
        if(cDe in self.cascaDe):
            for C in self.cascaDe[cDe]:
                r = C[0]
                c = C[1]
                if(isinstance(r,str) == True):
                    r = ord(r) - ord('a')
                if(isinstance(c,str) == True):
                    c = int(c)
                self.evaluate((r,c))
                value = self.cells2D[r][c].value
                self.updateSymTab(r,c,value)
                self.cascade((r,c))
                self.setLabel(frame = self.daBoard, row = r, col = c)
        
        

    def __repr__(self):
        lStr = ""
        for i in self.cells2D:
            lStr += "["
            for c in i:
                lStr += str(c.value)
                lStr += ","
            lStr = lStr[:-1]
            lStr += "]\n"
        return lStr

    def __str__(self):
        lStr = ""
        #if(neighbors == False):
        for i in self.cells2D:
            lStr += "["
            for c in i:
                lStr += str(c.value)
                lStr += ","
            lStr = lStr[:-1]
            lStr += "]\n"            
        return lStr



        
