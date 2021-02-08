# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 10:30:08 2021

@author: prami
"""

from enum import Enum
#import p5
from p5 import *
#from p5 import background,stroke,fill,rect,run,font,stroke_weight,line

#from p5 import text, text_font, text_size ,create_font

FONT = create_font("SigmarOne-Regular.ttf",0)

class Mark(Enum):
    X = 2
    O = 4
    EMPTY = 8

class State(Enum):
    Draw = 1
    Ongoing = 2
    Over = 3

#ttb= tictacboard
class ttb: 
    
    def __init__(self,size):
        #Size of the board and individual block 
        self.size = size
        self.size_per_square = self.size/3
        
        self.boardMat = [[Mark.EMPTY.value for x in range(3)] for y in range(3)]
        
        #Initialize Play 
        self.turnToPlay = Mark.X
        self.mark_size = int(self.size_per_square/2)
        self.winningMarks = []
        self.state = State.Ongoing
        self.winner = None
        self.moves = []
        
    def draw(self):
        #Used for Drawing the board
        self.__draw_background()
        self.__draw_board_state()
        
    def getTurn(self):
        return self.turnToPlay
    
    def getState(self):
        return self.state
    
    def getWinner(self):
        return self.winner 
    
    def getBoard(self):
        return self.boardMat
    
    def getPossibleMoves(self):
        
        possibleMoves=[]
        
        for i in range(0,3):
            for j in range(0,3):
                if self.boardMat[i][j] is Mark.EMPTY.value:
                    possibleMoves.append((i,j))
        
        return possibleMoves
    
    def __draw_background(self):
        stroke_weight(5)
        stroke(0)
        line((self.size_per_square, 0), (self.size_per_square, self.size))
        line((self.size_per_square * 2, 0), (self.size_per_square * 2, self.size))
        line((0, self.size_per_square), (self.size, self.size_per_square))
        line((0, self.size_per_square * 2), (self.size, self.size_per_square * 2))
        
    def __draw_board_state(self):
        
        for i in range (0,3):
            for j in range (0,3):
                state = Mark(self.boardMat[i][j])
                
                if state is not Mark.EMPTY:
                    text_font(FONT)
                    text_size(self.mark_size)
                    
                    if (i,j) in self.winningMarks:
                        fill(127,0,0)
                    else: 
                        fill(255)
                    text(state.name, (self.size_per_square * i + self.size_per_square / 2 - self.mark_size / 2, self.size_per_square * j + self.size_per_square / 2 - self.mark_size))

    def make_ui_move(self, mouse_x, mouse_y):
        if (self.state is State.Over):
            return

        x = int(mouse_x / self.size_per_square)
        y = int(mouse_y / self.size_per_square)
        self.make_move((x,y))

    def make_move(self,coordoninates):
       x = coordoninates[0]
       y = coordoninates[1]
       
       if (self.boardMat[x][y] == Mark.EMPTY.value):
           
           self.boardMat[x][y] = self.turnToPlay.value
           self.__switchPlayers()
           self.__updateBoardState()
           self.moves.append(coordoninates)
           
    def undo(self):
        lastMove = self.moves.pop()
        
        if lastMove:
            self.boardMat[lastMove[0]][lastMove[1]] = Mark.EMPTY.value
            self.__switchPlayers()
            self.__updateBoardState()
            
    def __updateBoardState(self):
        boardEval = self.evaluateBoardState()
        self.state = boardEval[0]
        self.winningMarks=[]
        self.winner = None
        
        if(self.state is State.Over):
            self.winningMarks = boardEval[2:]
            self.winner = boardEval[1]
            
    def __switchPlayers(self):
        self.turnToPlay = Mark.X if self.turnToPlay is Mark.O else Mark.O
    
    def evaluateBoardState(self):
        draw = True
        
        for x in range(0,3):
            for y in range(0,3):
                mark = Mark(self.boardMat[x][y])
                if mark is Mark.EMPTY:
                    draw = False
                    continue
                else:
                    #Check Horizontal Win
                    try:
                        if(mark.value | self.boardMat[x+1][y] | self.boardMat[x+2][y]) == mark.value:
                            return(State.Over, mark, (x,y),(x+1,y),(x+2,y))
                    except:
                        pass
                    
                    #Check Vertical Win
                    try:
                        if(mark.value | self.boardMat[x][y+1] | self.boardMat[x][y+2]) == mark.value:
                            return(State.Over, mark, (x,y),(x, y+1),(x,y+2))
                    except:
                        pass
                    
                    # Check for Diagonal Win
                    
                    if x==0 and y==0 and (mark.value | self.boardMat[x+1][y+1] | self.boardMat[x+2][y+2] == mark.value):
                        return(State.Over, mark, (x,y),(x+1,y+1),(x+2,y+2))
                    
                    elif x==0 and y==2 and (mark.value | self.boardMat[x+1][y-1] | self.boardMat[x+2][y-2] == mark.value):
                        return (State.Over, mark, (x,y),(x+1,y-1), (x+2,y-2))
       
        #If none of the above is true then , its a draw match
        return [State.Draw if draw else State.Ongoing]
                            
                    
         
            