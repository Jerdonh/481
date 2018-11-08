# ! / usr / bin / env python3

#Jerdon Helgeson
#HW5
#tictactoe

from tkinter import Tk
from tkinter import Frame
from tkinter import Button
from tkinter import *
from time import sleep

# Insert code for TicTacToeBoard or import it from a separate module.
# Your choice.


class TicTacToeBoard(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.board = {'A1':" ",'A2':" ",'A3':" ",
                      'B1':" ",'B2':"X",'B3':" ",
                      'C1':" ",'C2':" ",'C3':" "}
        self.clockwise = {'A1':"B1",'B1':"C1",'C1':"C2",'C2':"C3",'C3':"B3",'B3':"A3",'A3':"A2",'A2':"A1"}
        self.opposite = {'A1':'C3','B1':'B3','C1':'A3','A2':'C2','C2':'A2','A3':'C1','B3':'B1','C3':'A1'}
        self.usrTurn = True
        self.move = 1
        self.prevMove = 'B2'
        self.prevPrevMove = " "
        self.endGame = False
        self.difficulty = "Hard"
        self.message = Label(text = "message")
        buttFont = ('Verdana')#, "20")
        self.A1 = Button(self, text="", font=buttFont, command= lambda: self.update("A1"))
        self.A2 = Button(self, text="", font=buttFont, command= lambda: self.update("A2"))
        self.A3 = Button(self, text="", font=buttFont, command= lambda: self.update("A3"))
        self.B1 = Button(self, text="", font=buttFont, command= lambda: self.update("B1"))
        self.B2 = Button(self, text="X", font=buttFont, command= lambda: self.update("B2"))
        self.B3 = Button(self, text="", font=buttFont, command= lambda: self.update("B3"))
        self.C1 = Button(self, text="",font=buttFont,command= lambda: self.update("C1"))
        self.C2 = Button(self, text="",font=buttFont,command= lambda: self.update("C2"))
        self.C3 = Button(self, text="",font=buttFont,command= lambda: self.update("C3"))
        self.quitButton = Button(self, text="Quit",command= self.quit)
        """#I Tried to make different difficulties but not worth the effort I think
        self.var = StringVar()
        self.var.set("Hard") # default value
        self.var.trace("diffMenu", self.changeDiff)
        self.diffMenu = OptionMenu(self, "difficulty", "Normal", "Hard")"""
        self.buildBoard()

    def buildBoard(self):
        self.pack(fill=BOTH, expand=1)
        self.message.place(x = 0, y= 270)
        self.A1.config(height = 5, width = 8)
        self.A1.place(x = 0,y = 0)
        self.A2.config(height = 5, width = 8)
        self.A2.place(x = 0,y = 83)
        self.A3.config(height = 5, width = 8)
        self.A3.place(x = 0,y = 167)
        self.B1.config(height = 5, width = 8)
        self.B1.place(x = 75,y = 0)
        self.B2.config(height = 5, width = 8)
        self.B2.place(x = 75,y = 83)
        self.B3.config(height = 5, width = 8)
        self.B3.place(x = 75,y = 167)
        self.C1.config(height = 5, width = 8)
        self.C1.place(x = 150,y = 0)
        self.C2.config(height = 5, width = 8)
        self.C2.place(x = 150,y = 83)
        self.C3.config(height = 5, width = 8)
        self.C3.place(x = 150,y = 167)
        self.quitButton.place(x = 190,y = 270)

    def update(self, buttonPressed):
        txt = buttonPressed + " pressed"
        butt = getattr(self, buttonPressed) #ha. butt.
        if(self.usrTurn and butt['text'] == "" and self.endGame == False):
            self.move += 1
            self.prevPrevMove = self.prevMove
            self.prevMove = buttonPressed
            self.board[buttonPressed] = "O"
            butt.config(text = "O")
            self.usrTurn = False
            #print("Update fired: ", txt)
            print(self)
            if(self.move >= 5):
                win = self.checkGame()
                #print("CheckGame: ", win)
                if(win != None):
                    #print("Win: ", win)
                    self.gameOver(win)
                elif(win == None and self.move >= 9):
                    self.gameOver(win)
            if(self.endGame == False):
                self.message.config(text = "Computer's Turn")
                self.computerPlay()

    def changeDiff(self):
        self.difficulty = var.get()

    def computerPlay(self):
        #computer logic here
        pM = self.prevMove
        if(self.move == 2):
            #computer moves clockwise 1
            cw = self.getClockwise(pM)
            (getattr(self, cw)).config(text = "X")
            self.move += 1
            self.board[cw] = 'X'
            self.prevPrevMove = self.prevMove
            self.prevMove = cw
        else:
            #opposite
            #is users last move opposite to my last move? if not cmp wins else go clocwise again
            op = self.getOpposite(self.prevPrevMove)
            #print(op)
            if(self.board[op] != "X" and self.board[op] != "O"):
                (getattr(self, op)).config(text = "X")
                self.move += 1
                self.board[op] = 'X'
                self.prevPrevMove = self.prevMove
                self.prevMove = op
            else:
                cwB = "GOCOUGS"
                pM = self.prevMove
                while(cwB != " "):
                    cw = self.getClockwise(pM)
                    cwB = self.board[cw]
                    
                    if(cwB == " "):
                        (getattr(self, cw)).config(text = "X")
                        self.board[cw] = 'X'
                        self.move += 1
                        self.prevPrevMove = self.prevMove
                        self.prevMove = cw
                        break
                    else:
                        pM = self.getClockwise(pM)
                
            
        print(self)
        if(self.endGame == False):
            win = self.checkGame()
            if(win != None):
                self.gameOver(win)
            elif(win == None and self.move >= 9):
                self.gameOver(win)
            if(self.move < 9 and self.endGame == False):
                self.usrTurn = True
                self.message.config(text = "Your Turn")
            else:
                win = self.checkGame()
                self.gameOver(win)
            

            

    def getClockwise(self, pM):
        return self.clockwise[pM]

    def getOpposite(self, pM):
        #if(self.board[self.opposite[pM]] == " "):
        return self.opposite[pM]

    
    def checkGame(self):
        if  ( self.board['A1'] != " " and self.board['B1'] == self.board['A1'] and self.board['A1'] == self.board['C1']):
            #print("Win Detected: A1-B1-C1" )
            return self.board['A1']            
        elif (self.board['A1'] != " " and self.board['B2'] == self.board['A1'] and self.board['A1'] == self.board['C3']):
            #print("Win Detected: A1-B2-C3")
            return self.board['A1']
        elif (self.board['A1'] != " " and self.board['A1'] == self.board['A2'] and self.board['A1'] == self.board['A3']):
            #print("Win Detected: A1-A2-A3")
            return self.board['A1']
        elif(self.board['A2'] != " " and self.board['A2'] == self.board['B2'] and self.board["A2"] == self.board['C2']):
            #print("Win Detected: A2-B2-C2")
            return self.board['A2']
        elif(self.board['A3'] != " " and self.board['A3'] == self.board['B3'] and self.board["A3"] == self.board['C3']):
            #print("Win Detected: A3-B3-C3")
            return self.board['A3']
        elif(self.board['B1'] != " " and self.board['B1'] == self.board['B2'] and self.board['B1'] == self.board['B3']):
            #print("Win Detected: B1-B2-B3")
            return self.board['B1']
        elif(self.board['C1'] != " " and self.board['C1'] == self.board['C2'] and self.board["C1"] == self.board['C3']):
            #print("Win Detected: C1-C2-C3")
            return self.board['C1']
        elif(self.board['C1'] != " " and self.board['C1'] == self.board['B2'] and self.board["C1"] == self.board['A3']):
            #print("Win Detected: C1-B2-A3")
            return self.board['C1']
        else:
            return None

    def gameOver(self, winner = None):
        self.endGame = True
        #print("GameOver: ", winner)
        if(winner != None):
            if(winner == "X"):
                #print("winner == X")
                self.message.config(text = "Game Over : Computer Wins")
            elif(winner == "O"):
                #print("winner == O")
                self.message.config(text = "You Win")
        else:
            self.message.config(text = "Cats Game")
        

    def quit(self):
        quit()

    def __str__(self):
        toPrint = self.board['A1']+'|'+self.board['B1']+'|'+self.board['C1'] + "\n"
        toPrint += "______\n"
        toPrint += self.board['A2']+'|'+self.board['B2']+'|'+self.board['C2']+"\n"
        toPrint += "______\n"
        toPrint += self.board['A3']+'|'+self.board['B3']+'|'+self.board['C3']+"\n"
        return toPrint
        


root = Tk()
root.title("Tic Tac Toe")
root.geometry("225x315")
label1 = Label(root, text="message", width=len("message"))
board = TicTacToeBoard(root)
#board.grid()

root.mainloop()
