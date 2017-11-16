class Tile:

    
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.blank = ( (x,y) in [(0,-1), (-1,0), (1,1)] )
        self.colour = 0
        if (x, y) in [(4,0), (-4,-4), (0,4)]:
            self.colour = 1
        elif (x,y) in [(-4,0), (0,-4), (4,4)]:
            self.colour = 2
        
        self.neighbours=[]
        if not (x == -4 or x-y == -4):
            self.neighbours.append((x-1, y))
        if not (x == 4 or x-y == 4):
            self.neighbours.append((x+1, y))
        if not (y == -4 or x-y == 4):
            self.neighbours.append((x, y-1))
        if not (y == 4 or x-y == -4):
            self.neighbours.append((x, y+1))
        if not (x == -4 or y == -4):
            self.neighbours.append((x-1, y-1))
        if not (x == 4 or y == 4):
            self.neighbours.append((x+1, y+1))

        self.far_neighbours=[]
        #cornery:
        if not (x <= -3 or x-y <= -3):
            self.far_neighbours.append((x-2, y))
        if not (x >= 3 or x-y >= 3):
            self.far_neighbours.append((x+2, y))
        if not (y <= -3 or x-y >= 3):
            self.far_neighbours.append((x, y-2))
        if not (y >= 3 or x-y <= -3):
            self.far_neighbours.append((x, y+2))
        if not (x <= -3 or y <= -3):
            self.far_neighbours.append((x-2, y-2))
        if not (x >= 3 or y >= 3):
            self.far_neighbours.append((x+2, y+2))
        #edgy:
        if not (x <= -3 or y == -4 or x-y == -4):
            self.far_neighbours.append((x-2, y-1))
        if not (x >= 3 or y == 4 or x-y == 4):
            self.far_neighbours.append((x+2, y+1))
        if not (y <= -3 or x == -4 or x-y == 4):
            self.far_neighbours.append((x-1, y-2))
        if not (y ==4 or x == -4 or x-y <= -3):
            self.far_neighbours.append((x-1, y+1))
        if not (x == -4 or y == 4 or x-y <= -3):
            self.far_neighbours.append((x-1, y+1))
        if not (x == 4 or y == -4 or x-y >= 3):
            self.far_neighbours.append((x+1, y-1))
        

    def put_gem(self, colour):
        if self.colour == 0:
            self.colour = colour
        else:
            print("Error! attempt to put gem on occupied tile")

    def zap(self, colour):
        if self.colour != 0:
            self.colour = colour

    def empty(self):
        self.colour = 0
            


class Board:

    def __init__(self):
        self.tiles = []
        self.tile_lookup = {}


        for x in range(-4, 5):
            for y in range(max(-4,x-4), min(5,x+5)):
                t = Tile(x,y)
                self.tiles.append(t)
                self.tile_lookup[(x,y)] = t

    def clone(self, source, target):
        if (target.x, target.y) in source.neighbours and not target.blank:
            target.put_gem(source.colour)
            for t in target.neighbours:
                self.tile_lookup[t].zap(source.colour)
        else:
            print("Error! attempt to clone to illegal tile")

    def jump(self, source, target):
        if (target.x, target.y) in source.far_neighbours and not target.blank:
            target.put_gem(source.colour)
            for t in target.neighbours:
                self.tile_lookup[t].zap(source.colour)
            source.empty()
        else:
            print("Error! attempt to jump to illegal tile")

    def get_scores(self):
        s1, s2 = 0, 0
        for t in self.tiles:
            if t.colour == 1:
                s1 += 1
            elif t.colour == 2:
                s2 +=1
        return (s1, s2)

    def is_full(self):
        e = 0
        for t in self.tiles:
            if t.colour == 0 and not t.blank:
                e +=1
        return e==0
        
