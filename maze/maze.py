import pygame,os
from pygame import *
import maze_algo
import time as _time
import random

#RGB
BLACK = (0,0,0)
GRAY = (100,100,100)
NAVYBLUE = (60,60,100)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,128,0)
PURPLE = (255,0,255)
CYAN = (0,255,255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

WIN_WIDTH = 200
WIN_HEIGHT = 150
HALF_WIDTH = int(WIN_WIDTH/2)
HALF_HEIGHT = int(WIN_HEIGHT/2)

DISPLAY = (WIN_WIDTH,WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30
t0,t1 = 0,0
Elapsed_time = 0
END_FLAG = 0
coincount = 0
player_ch = 0
B = 0

def main(_lv):
    global cameraX,cameraY,screen,B
    B = random.randrange(1,3)
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY,FLAGS,DEPTH)
    pygame.display.set_caption("Maze")
    timer = pygame.time.Clock()

    up = down = left = right = running = False
    bg = Surface((32,32))
    bg.convert()
    bg.fill(WHITE)
    entities = pygame.sprite.Group()
    player = Player(32,32)
    platforms = []

    x = y = 0
    Tmp = int(_lv/3)
    rtmp = (Tmp*6) + 10
    ctmp = (Tmp*4) + 10
    level = maze_algo.make_maze(rtmp,ctmp)
    for row in level:
        for col in row:
            if col == "+" or col=="-" or col=="|":
                p = Platform(x,y)
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = ExitBlock(x,y)
                platforms.append(e)
                entities.add(e)
            if col == "C":
                c = CoinBlock(x,y)
                platforms.append(c)
                entities.add(c)
            x += 32
        y += 32
        x = 0

    total_level_width = len(level[0])*32
    total_level_height = len(level)*32
    camera = Camera(complex_camera,total_level_width,total_level_height)
    entities.add(player)

    exit_flag = 0
    global t0
    t0 = _time.time()
    while True:
        timer.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT: raise SystemExit
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                running = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == QUIT:
                exit_flag = 1
        if exit_flag: break
        if END_FLAG == 1:
            global Elapsed_time
            et = round(Elapsed_time,3)
            break
        else:
            for y in range(32):
                for x in range(32):
                    screen.blit(bg,(x*32,y*32))
            camera.update(player)
            player.update(up,down,left,right,running,platforms)
            for e in entities:
                screen.blit(e.image,camera.apply(e))

        pygame.display.update()
    print(" => Your Speed : "+ str(et) + "seconds")
    pygame.quit()


def initial_start():
    global t0,t1,Elapsed_time,END_FLAG,coincount
    t0,t1 = 0,0
    Elapsed_time = 0
    END_FLAG = 0
    coincount = 0
    startImg = pygame.image.load('src/start.png')
    screen = pygame.display.set_mode(DISPLAY)
    screen.blit(startImg,(0,0))
    pygame.display.set_caption("Maze")
    pygame.display.update()
    while True:
        for e in pygame.event.get():
            if e.type == KEYDOWN and e.key == K_SPACE: return 0


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           
    l = max(-(camera.width-WIN_WIDTH), l)   
    t = max(-(camera.height-WIN_HEIGHT), t) 
    t = min(0, t)                           
    return Rect(l, t, w, h)


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.image = pygame.image.load('src/ch/'+str(player_ch)+'.png')
        self.rect = Rect(x, y, 20, 20)

    def update(self, up, down, left, right, running, platforms):
        if up:
            self.yvel = -8
        if down:
            self.yvel = 8
        if running:
            self.xvel = 12
        if left:
            self.xvel = -8
        if right:
            self.xvel = 8
        if not(left or right):
            self.xvel = 0
        if not(up or down):
            self.yvel = 0
        self.rect.left += self.xvel
        self.collide(self.xvel, 0, platforms)
        self.rect.top += self.yvel
        self.collide(0, self.yvel, platforms)


    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    global t1
                    global t0
                    global Elapsed_time,END_FLAG
                    t1 = _time.time()
                    Elapsed_time = t1-t0
                    END_FLAG = 1
                    #pygame.event.post(pygame.event.Event(QUIT))
                if isinstance(p, CoinBlock):
                    global coincount
                    coincount += 1
                    platforms.remove(p.rect)
                    p.kill()
                if xvel > 0:
                    self.rect.right = p.rect.left
                    #print("collide right")
                if xvel < 0:
                    self.rect.left = p.rect.right
                    #print("collide left")
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    #print("collide bottom")
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    #print("collide top")


class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        #self.image = Surface((32, 32))
        #self.image.convert()
        #self.image.fill(Color("#DDDDDD"))
        global B
        self.image = pygame.image.load('src/ch/block'+str(B)+'.png')
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load('src/finish.png')
        #self.image.fill(Color("#0033FF"))

class CoinBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = pygame.image.load('src/coin.png')
        #self.image.fill(Color("#0033FF"))

def start_maze(user):
    global player_ch
    player_ch = user.character
    initial_start()
    main(user.level)
    rtlist = []
    global Elapsed_time
    et = round(Elapsed_time,3)
    rtlist.append(et)
    global coincount
    rtlist.append(user.coin + coincount)
    player_ch = 0
    return rtlist

    




            
            
