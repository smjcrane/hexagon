import GUI
from boardmaker import *
import random
import random_player
import human_player

def play_game(player1, player2):
    board = Board()
    GUI.setupDrawing()
    GUI.update(board)
    progress = True
    while (progress):
        player1.play(board, 1)
        GUI.update(board)
        progress = not board.is_full()
        player2.play(board, 2)
        GUI.update(board)
        progress = not board.is_full()   
    return board.get_scores()
        


print play_game(random_player, random_player)
