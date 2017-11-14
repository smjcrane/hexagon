import random

def play(board, colour):
    mine = []
    allowed = []
    for t in board.tiles:
        if t.colour == colour:
            mine.append(t)
    for t in mine:
        for n in t.neighbours:
            m = board.tile_lookup[n]
            if m.colour == 0:
                allowed.append((t, m))
    if len(allowed) > 0:
        move = random.choice(allowed)
        board.clone(move[0], move[1])
