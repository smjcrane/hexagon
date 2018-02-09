import random

def play(board, colour):
    mine = []
    allowed_clones = []
    allowed_jumps = []
    for t in board.tiles:
        if t.colour == colour:
            mine.append(t)
    for t in mine:
        for n in t.neighbours:
                m = board.tile_lookup[n]
                if m.colour == 0 and not m.blank:
                    allowed_clones.append((t, m))
        for f in t.far_neighbours:
                m = board.tile_lookup[f]
                if m.colour == 0 and not m.blank:
                    allowed_jumps.append((t, m))
    if len(allowed_clones) == 0:
        if len(allowed_jumps) == 0:
            return
        else:
            move = random.choice(allowed_jumps)
            board.jump(move[0], move[1])
            return ( (move[0].x, move[0].y) , (move[1].x, move[1].y), "j" )  
    elif len(allowed_jumps) == 0:
        move = random.choice(allowed_clones)
        board.clone(move[0], move[1])
        return ( (move[0].x, move[0].y) , (move[1].x, move[1].y), "c" ) 
    else:
        move_type = random.randint(0,1)
        if move_type:
            move = random.choice(allowed_jumps)
            board.jump(move[0], move[1])
            return ( (move[0].x, move[0].y) , (move[1].x, move[1].y), "j" ) 
        else:
            move = random.choice(allowed_clones)
            board.clone(move[0], move[1])
            return ( (move[0].x, move[0].y) , (move[1].x, move[1].y), "c" ) 
