import visual as v
from visual.graph import curve
from boardmaker import *

def setupDrawing():
	v.scene.autoscale = 1
	v.scene.center=(0,0,0)
	seperation=100
	wood = v.box(pos =(0, 0, -1), size = (1000-seperation, 1000-seperation, 2), color=(0.7, 0.4, 0.1))
	axes = []
	
	corners = [(4,0), (0,-4), (-4,-4), (-4,0), (0,4), (4,4), (4,0)]
        #edges of the board
	for i in range(len(corners)-1):
                r0 = corners[i][0] * (3**0.5) / 2.0
                c0 = corners[i][1] - 0.5*corners[i][0]
                
                r1 = corners[i+1][0] * (3**0.5) / 2.0
                c1 = corners[i+1][1] - 0.5*corners[i+1][0]
                
                axes.append( curve(pos=[(c0*seperation, r0*seperation, 1), (c1*seperation, r1*seperation, 1)], color=(1,0,0))  )

        #lines of constant y
	for y in range(-3, 4):
                if y<0:
                        x0 = -4
                        x1 = 4+y
                else:
                        x0 = y-4
                        x1 = 4

                r0 = x0 * (3**0.5) / 2.0
                c0 = y - 0.5*x0
                
                r1 = x1 * (3**0.5) / 2.0
                c1 = y - 0.5*x1
                
                axes.append( curve(pos=[(c0*seperation, r0*seperation, 1), (c1*seperation, r1*seperation, 1)], color=(1,1,1))  )
                #Do the y-x=constant lines at the same time by reflecting in the y axis
                axes.append( curve(pos=[(c0*seperation, -r0*seperation, 1), (c1*seperation, -r1*seperation, 1)], color=(1,1,1))  )

	#lines of constant x
        for x in range(-3, 4):
                if x<0:
                        y0 = -4
                        y1 = 4+x
                else:
                        y0 = x-4
                        y1 = 4

                r0 = x * (3**0.5) / 2.0
                c0 = y0 - 0.5*x
                
                r1 = x * (3**0.5) / 2.0
                c1 = y1 - 0.5*x
                
                axes.append( curve(pos=[(c0*seperation, r0*seperation, 1), (c1*seperation, r1*seperation, 1)], color=(1,1,1))  )


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



