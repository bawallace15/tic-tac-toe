import sys, pygame
import numpy as np
pygame.init()

class player():
    def __init__(self, name, img):
        self.name = name
        self.img = img
        self.taken = np.zeros((3,3), dtype=bool)

def draw_boundary(coord):
    pygame.draw.line(screen, black, coord[0], coord[1], 1)

def form_area(coord):
    area = pygame.Rect(int(coord[0]), int(coord[1]), int(coord[2]), int(coord[3]))
    return area

def clicked_area(pos, areas):
    for i in np.arange(len(areas)):
        if areas[i].collidepoint(pos):
            return i
    print('Failed to find area')
    return False

def swapTurn(turn):
    if turn == 0:
        turn = 1
    else:
        turn = 0
    return turn

def checkRows(board):
    for row in board:
        if True in set(row) and len(set(row)) == 1:
            return True
    return False

def checkColumns(board):
    for row in board.T:
        if True in set(row) and len(set(row)) == 1:
            return True
    return False

def checkDiagonals(board):
    if board.shape == 2 and board.shape[0]:
        print('matrix is not 2D or square')
        pygame.quit()
    diag1 = True
    diag2 = True
    for i in np.arange(board.shape[0]):
        # one diag always has the ind equal
        if not board[i, i]:
            diag1 = False
        # the other is equal to len side - ind (-1 bc 0 indx)
        if not board[i, (board.shape[0]-1)-i]:
            diag2 = False
    return diag1 or diag2

def checkWin(board):
    if checkRows(board) or checkColumns(board) or checkDiagonals(board):
        return True
    return False

speed = [10, 1]
black = (0,0,0)
white = (255,255,255)
border = (20,15)

# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])

# Should combine boundaries and zones
boundaries = [[[0,600/3],[800,600/3]], 
[[0,600/3*2],[800,600/3*2]],
[[800/3,0],[800/3,600]],
[[800/3*2,0],[800/3*2,600]]]

zones = [(0, 0, 800/3, 600/3),
(800/3, 0, 800/3, 600/3),
(800/3*2, 0, 800/3, 600/3),
(0, 600/3, 800/3, 600/3),
(800/3, 600/3, 800/3, 600/3),
(800/3*2, 600/3, 800/3, 600/3),
(0, 600/3*2, 800/3, 600/3),
(800/3, 600/3*2, 800/3, 600/3),
(800/3*2, 600/3*2, 800/3, 600/3)]

zone_map = {}
zone_map[0] = [0,0]
zone_map[1] = [0,1]
zone_map[2] = [0,2]
zone_map[3] = [1,0]
zone_map[4] = [1,1]
zone_map[5] = [1,2]
zone_map[6] = [2,0]
zone_map[7] = [2,1]
zone_map[8] = [2,2]

pximg = pygame.image.load(r'./X.png')
poimg = pygame.image.load(r'./O.png')

pximg = pygame.transform.scale(pximg, (int(800/3)-border[0],int(600/3)-border[1]))
poimg = pygame.transform.scale(poimg, (int(800/3)-border[0],int(600/3)-border[1]))

players = []
players.append(player('x',pximg))
players.append(player('o',poimg))

clock = pygame.time.Clock()
    
screen.fill(white)
for bound in boundaries:
    draw_boundary(bound)

areas = []
for i in np.arange(len(zones)):
    areas.append(form_area(zones[i]))

# this it the player # whose turn it is
turn = 0
# this is a list of taken spaces
taken = []
while 1:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            ind = clicked_area(event.pos, areas)
            if ind in taken:
                continue
            else:
                screen.blit(players[turn].img, (areas[ind][0]+border[0]/2,areas[ind][1]+border[1]/2))
                taken.append(ind)
                players[turn].taken[zone_map[ind][0], zone_map[ind][1]] = True
                win = checkWin(players[turn].taken)
                if win:
                    print('WIN Player ' + str(turn))
                    pygame.quit()
                turn = swapTurn(turn)

    pygame.display.flip()

pygame.quit()