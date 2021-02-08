# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 14:22:06 2021

@author: prami
"""

from board import ttb, State, Mark
#from p5 import background,stroke,fill,rect,run, mouse_is_pressed, mouse_x, mouse_y
import math
import p5
from p5 import *

myBoard = None
SIZE = 300
playAs  = Mark.X
aiPlay = Mark.X if playAs == Mark.O else Mark.O

def setup():
    global myBoard
    size = (SIZE,SIZE)
    background(204)
    myBoard = ttb(SIZE)
    
def draw():
    size_per_square = SIZE/3
    myBoard.draw()
    
    if myBoard.getState() is not State.Ongoing:
        return
    
    if (myBoard.getTurn() is aiPlay):
        bestScore = -math.inf
        bestMove = None
        
        for move in myBoard.getPossibleMoves():
            myBoard.make_move(move)
            score = minimax(False, aiPlay, myBoard)
            myBoard.undo()
            
            if(score > bestScore):
                bestScore = score
                bestMove = move
                
        myBoard.make_move(bestMove)
    
    else:
        if mouse_is_pressed:
            myBoard.make_ui_move(mouse_x, mouse_y)

def minimax (isMaxTurn, maximizerMark, board):
    
    state = board.getState()
    
    if (state is State.Draw):
        return 0
    elif state is State.Over:
        return 1 if board.getWinner() is maximizerMark else -1
    
    scores = []
    
    for move in board.getPossibleMoves():
        board.make_move(move)
        
        scores.append(minimax(not isMaxTurn, maximizerMark, board)) 
        board.undo()
        
        if (isMaxTurn and max(scores)==1) or (not isMaxTurn and min(scores)==-1):
            break
        
    return max(scores) if isMaxTurn else min(scores)

run()
    


        
        
        
        