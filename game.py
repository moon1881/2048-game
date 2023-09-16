import pygame
import random
import math
from pygame import mixer
pygame.init()


#Setting the display and title to game
width = 500
height = 500
display = pygame.display.set_mode([width,height])
pygame.display.set_caption("Space 2048 game!")
font = pygame.font.Font("ModernWarfare-OV7KP.ttf",20)
time = pygame.time.Clock()
fps=60
#load the bg (image) and icon
bg = pygame.image.load("star.jpg").convert()
icon = pygame.image.load('icon.jpg')
pygame.display.set_icon(icon)
bgW = bg.get_width()
# load bg music
mixer.music.load("stars2.wav")
mixer.music.play(-1)
#variables
scroll = 0
tiles = math.ceil(width/bgW)+1
values = [[0 for _ in range (4)] for _ in range(4)]
g_over = False
s_new = True
in_count = 0
direction =''
score = 0
high_score=0


#restart the game after game over:
def draw_back():
    pygame.draw.rect(display,colors[6],[80,200,350,100],0,10)
    text = font.render("Game Over!!",True,colors['black'])
    text2 = font.render("Press Enter to restart",True,colors['black'])
    display.blit(text,(170,220))
    display.blit(text2,(100,260))
    pygame.display.update()
    
    


# turns (direction)
def take_turn(d,board):
    global score 
    merge = [[False for _ in range (4)] for _ in range(4)]
    if d == 'UP':
        for i in range(4):
            for j in range (4):
                move = 0
                if i>0:
                    for q in range (i):
                        if board[q][j]==0:
                            move=move+1
                    if move > 0:
                        board[i-move][j] = board[i][j]
                        board[i][j]= 0
                    if board[i - move -1][j] == board[i-move][j] and not merge[i-move-1][j] \
                    and not merge[i - move][j]:
                        board[i-move-1][j] *=2
                        score += board[i-move-1][j] 
                        board[i - move][j]=0
                        merge[i-move-1][j]=True

    elif d == 'DOWN':
        for i in range (3):
            for j in range(4):
                move = 0
                for q in range (i+1):
                    if board[3-q][j]==0:
                        move = move +1
                if move > 0:
                    board[2-i+move][j] = board[2-i][j]
                    board[2-i][j]=0
                if 3 - i +move <=3:
                    if board[2-i+move][j] == board[3-i+move][j] and not merge[3-i+move][j] \
                    and not merge[2-i+move][j]:
                        board[3-i + move][j] = board[3-i+move][j]* 2
                        score += board[3-i + move][j]
                        board[2-i+move][j]=0
                        merge[3-i+move][j] = True
                       
    elif d == 'LEFT':
        for i in range (4):
            for j in range(4):
                move = 0
                for q in range (j):
                    if board[i][q] == 0:
                        move = move +1
                if move>0:
                    board[i][j-move] = board[i][j]
                    board[i][j] = 0
                if board[i][j-move] == board[i][j-move-1] and not merge[i][j-move-1] \
and not merge[i][j-move]:
                    board[i][j-move-1] *=2
                    score += board[i][j-move-1]
                    board[i][j-move]=0
                    merge[i][j-move -1]=True
    elif d == 'RIGHT':
        for i in range(4):
            for j in range(4):
                move=0
                for q in range(j):
                    if board[i][3-q] == 0:
                        move = move+1
                if move>0:
                    board[i][3-j+move] = board[i][3-j]
                    board[i][3-j]=0
                if 4-j+move<=3:
                    if board[i][4-j+move] == board[i][3-j+move] and not merge[i][4-j+move] \
                            and not merge[i][3-j+move]:
                        board[i][4-j+move]  *=2
                        score += board[i][4-j+move]
                        board[i][3-j+move] = 0
                        merge[i][4-j+move] = True

    return board

#put pieces on board as a start
def new(board):
    count=0
    over = False
    while any(0 in row for row in board) and count < 1: 
        row = random.randint(0,3)
        col = random.randint(0,3)
        if board[row][col]==0:
            count = count +1 
            if random.randint(1,10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count <1:
        over = True    
    return board,over
#colors used in the game
colors = {0:(211, 231, 237),
          2:(179, 217, 230),
          4:(152, 201, 217),
          8:(118, 177, 196),
          16:(87, 150, 171),
          32:(30, 139, 176),
          64:(23, 107, 135),
          128:(11, 82, 125),
          256:(9, 69, 105),
          512:(8, 59, 89),
          1024:(6, 44, 67),
          2048:(0,28,48),
          'black':(0,0,0),
          'bg':(19, 24, 28),
          5:(0,0,0),
          6:(255,255,255)}


# drawing the board 
def board():
    rect = pygame.Rect(80,80,350,350)
    rectangle= pygame.draw.rect(display,colors['bg'],rect)
    score_t = font.render(f'Score:{score}',True,colors[6])
    h_t = font.render(f'High Score:{high_score}',True,colors[6])
    display.blit(h_t,(10,450))
    display.blit(score_t,(10,470))
    
# drawing the tiles on board
def tile(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 32:
                value_color = colors[0]
            else:
                value_color = colors['black']
            if value <=2048:
                color = colors[value]
            else:
                color = (255,255,255)
            pygame.draw.rect(display,color,[j*95+75, i*95+75,75,75],0,10)
            if value > 0:
                length = len(str(value))
                font = pygame.font.Font("ModernWarfare-OV7KP.ttf",48-(7 * length))
                text = font.render(str(value),True,value_color)
                rec_text = text.get_rect(center = (j * 95 +112, i*95+112))
                display.blit(text,rec_text)
                pygame.draw.rect(display,colors['black'],[j*95+70, i*95+70,75,75],2,5)
# main game loop
running = True
while running:
    time.tick(fps)
    #scrolling bg
    for i in range(0,tiles):
        display.blit(bg,(i*bgW+scroll,0))
    scroll = scroll - 5
    if abs(scroll) > bgW:
        scroll=0
    board()
    tile(values)
    if s_new or in_count < 2:
        values , g_over = new(values)
        s_new = False
        in_count = in_count +1
    if direction != '':
        values = take_turn(direction,values)
        direction = ''
        s_new = True
    if g_over:
        draw_back()
        
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'
            if g_over:
                if event.key == pygame.K_RETURN:
                    values = [[0 for _ in range(4)] for _ in range(4)]
                    s_new =True
                    in_count = 0
                    score = 0
                    direction = ''
                    g_over = False
    if score > high_score:
        high_score=score
                
                
            

    pygame.display.update()
pygame.quit()
