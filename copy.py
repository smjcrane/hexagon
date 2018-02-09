
import GUI
from boardmaker import *
import random
import random_player
import human_player
import machine_learner as ml

def learn_from(player1, m):
    board = Board()
    if graphics:
        GUI.setupDrawing()
        GUI.update(board)
    progress = True
    i = 0
    while (progress):
        m.make_move(board)
        goal = player1.play(board, i % 2 + 1)
        if graphics:
            GUI.update(board)
        progress = not board.is_full()
        if goal != None:
            m.mimic(m.history[-1], m.moves.index(goal) )
        #else:
        #    #print "None"
        i+=1
    return board.get_scores()
        
m = ml.MachineLearner()
m.randomise_params()

graphics = False

for j in range(0, 10000):
    s = learn_from(random_player, m)
    if j % 100 == 0:
        m.regularise()
        m.save_params()
        print "saving"
    #print s

m.regularise()
m.save_params()
