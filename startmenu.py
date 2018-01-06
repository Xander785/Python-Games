import sys,random
import Game as g
import pygame as pg
class Mouse:
    def __init__(self):
        self.mouse = pg.Surface((20,20)).convert_alpha()
        self.mouse_rect = self.mouse.get_rect(center = pg.mouse.get_pos())
    def update(self,surface):
        coord = pg.mouse.get_pos()
        self.mouse.fill((0,0,0,0))
        pg.draw.circle(self.mouse,(255,255,255),(10,10),10)
        self.mouse_rect.center = coord
        surface.blit(self.mouse,self.mouse_rect)
class Laser:
    def __init__(self,y,ch):
        self.image = pg.image.load('laser.png').convert()
        self.image.set_colorkey((255,0,255))
        self.image = pg.transform.rotate(self.image,180)
        self.rect = self.image.get_rect(center =(0,y))
        ch.play(pg.mixer.Sound('pew.wav'))
    def update(self,screen):
        if self.rect.left > 1920:
            return True
        else:
            self.rect.x += 5
            screen.blit(self.image,self.rect)
            return False
class start:
    def __init__(self):
        self.screen = pg.display.set_mode((1920,1080),pg.FULLSCREEN)
        pg.mixer.init()
        pg.font.init()
        self.C1 = pg.mixer.Channel(0)
        self.C2 = pg.mixer.Channel(1)
        self.C3 = pg.mixer.Channel(2)
        self.bgmusic = pg.mixer.Sound('ninja.wav')
        self.explode = pg.mixer.Sound('explode.wav')
        self.mouse = Mouse()
        self.click0 = False
        self.lasers = []
        pg.mouse.set_visible(False)
        self.image = pg.image.load('background.jpg').convert_alpha()
        self.C1.play(self.bgmusic,-1)
        self.t = 1
        file = open('high','rb+')
        print(file)
        self.score = [0]
        for y in file:
            self.score.append(int(y))
        self.score.sort()
        print(self.score,'self.score')
    def title(self):
        txts = pg.font.SysFont('Courier New', 128).render('S p a c e S h o o t e r', True, (255,255,255))
        txtrect = txts.get_rect()
        txtrect.center = (960,80)
        self.screen.blit(txts,txtrect)
        txts = pg.font.SysFont('Courier New', 90).render('High Score: '+str(self.score[-1]), True, (255,255,255))
        txtrect = txts.get_rect()
        txtrect.center = (1600,200)
        txtrect.right = 1910
        self.screen.blit(txts,txtrect)
    def draw(self):
        for y in range(0,1080,168):
            for x in range(0,1920,300):
                self.screen.blit(self.image,(x,y))
        for x in self.lasers:
            a = x.update(self.screen)
            if a:self.lasers.remove(x)
        self.title()
        x = self.make_button()
        if x:
            click = pg.mouse.get_pressed()
            if click[0] == 1:
                self.click0 = True
            if self.click0 == True:
                if click[0] == 0:
                    self.start()
                    self.click0 = False
        txts = pg.font.SysFont('Courier New', 64).render('START', True, (255,255,255))
        txtrect = txts.get_rect()
        txtrect.center = (960,540)
        self.screen.blit(txts,txtrect)
        self.mouse.update(self.screen)
    def laser(self):
        if self.t%50 == 0:
            self.lasers.append(Laser(random.randint(10,1070),self.C3))
    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                sys.exit()
    def make_button(self):
        mouse = pg.mouse.get_pos()
        #cords
        #x 810
        #y 515
        #w 300
        #h 50
        if (1110) > mouse[0] > 810 and (590) > mouse[1] > 490:
            hover = True
            image = pg.image.load('start2.png').convert()
        else:
            image = pg.image.load('start1.png').convert()
            hover = False
        image.set_colorkey((255,0,255))
        rect = pg.Rect(810,490,300,50)
        self.screen.blit(image,rect)
        return hover
    def start(self):
        self.C1.stop()
        self.C2.play(self.explode)
        self.score = g.Game().loop()
        file = open('high','a')
        file.write(str(self.score)+'\n')
        file.close()
        file = open('high','rb+')
        self.score = [0]
        for y in file:
            self.score.append(int(y))
        self.score.sort()
        print(self.score,'self.score')
        pg.mixer.stop()
        self.C2.play(self.explode)
        self.C1.play(self.bgmusic,-1)
        self.lasers = []
        self.t = 0
    def loop(self):
        while 1:
            self.laser()
            self.draw()
            self.event()
            pg.display.update()
            self.t+=1

