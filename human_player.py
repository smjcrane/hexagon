def play(board, colour):
    a, b = map(int, raw_input("enter source: ").split(" "))
    c, d = map(int, raw_input("enter target: ").split(" "))
    board.clone(board.tile_lookup[(a,b)], board.tile_lookup[(c,d)])
