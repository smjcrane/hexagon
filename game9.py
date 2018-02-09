
import GUI
from boardmaker import *
import random
import random_player
import human_player
import machine_learner as ml

def play_game(player1, player2):
    board = Board()
    if graphics:
        GUI.setupDrawing()
        GUI.update(board)
    progress = True
    while (progress):
        player1.play(board, 1)
        if graphics:
            GUI.update(board)
        progress = not board.is_full()
        player2.play(board, 2)
        if graphics:
            GUI.update(board)
        progress = not board.is_full()   
    return board.get_scores()
        
m = ml.MachineLearner()
m.randomise_params()

graphics = True


for i in range(0, 100):
    s = play_game(random_player, m)
    print s
    m.back_propogate(s)
