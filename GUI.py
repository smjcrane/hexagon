import visual as v
from boardmaker import *

def setupDrawing():
	v.scene.autoscale = 1
	v.scene.center=(0,0,0)
	seperation=100
	wood = v.box(pos =(0, 0, -1), size = (1000-seperation, 1000-seperation, 2), color=(0.7, 0.4, 0.1))
	

def update(board):
	spheres=[]
	v.rate(5)
	try:
		clear()
	except:
		spheres=[]
		#print("nosphresexist")
	seperation=100
	for t in board.tiles:
                r = t.x * (3**0.5) / 2.0
                c = t.y - 0.5*t.x
                if t.colour == 1:
                        spheres.append( v.sphere(pos= (c*seperation, r*seperation, 0), color = (0.1,0.05,0.05), radius = seperation/2.5)  )
                if t.colour == 2:
                        spheres.append( v.sphere(pos= (c*seperation, r*seperation, 0), color = v.color.white, radius = seperation/2.5)  )

def clear():
	for obj in v.scene.objects:
		#print(obj)
		if isinstance(obj, v.sphere):
			obj.visible=False


def selectPlace(board):
    #raw_input(len(board))
    size=int((len(board))**0.5)
    ev=v.scene.waitfor("click")

    place=None
    for i in range(0,size):
        for j in range(0,size):
            if ev.pos[0]> 100*(i+1) -35 and ev.pos[0] < 100*(i+1)+35:
                if ev.pos[1]> 100*(j+1) -35 and ev.pos[1] < 100*(j+1)+35:
                    place=alpha[i]+numbers[j]
    return place


def makeMove(player, board, game_state):
    place=selectPlace(board)
    if place!= None:
        return place
    return "pass"



