import sys,math,random
import pygame as pg
BG = pg.Color('slategray')
class Player(pg.sprite.Sprite):
    def __init__(self,*groups):
        super(Player,self).__init__(*groups)
        self.pos = [500,500]
        self.hp = 200
        self.fullhp = 200
        self.original_image = pg.image.load('spaceship.png').convert()
        self.original_image.set_colorkey((255,0,255))
        #self.original_image.fill((0,0,255))
        self.image = self.original_image
        self.lasers = []
        self.color = (0,255,0)
        self.rect = self.image.get_rect(center = self.pos)
        self.mask = pg.mask.from_surface(self.image)
        self.a = pg.Surface((310,35))
        self.a.fill((0,0,0))
        self.ar =ar = pg.Rect(10,50,300,25)
    def hpdraw(self):
        hp_percent = int(round((self.hp/self.fullhp)*100,0))
        if hp_percent >=50:color=(0,255,0)
        elif 20<hp_percent<50:color=(255,255,0)
        else:color=(255,0,0)
        self.color = color
        txts = pg.font.SysFont('Courier New', 32).render(str(hp_percent)+'%', True, self.color)
        txtrect = txts.get_rect()
        txtrect.topleft = (10,10)
        self.hp_percent = hp_percent
        return txts,txtrect
    def rotate(self):
        mouse = pg.mouse.get_pos()
        offset = (mouse[1]-self.rect.centery, mouse[0]-self.rect.centerx)
        self.angle = 135-math.degrees(math.atan2(*offset))
        self.image = pg.transform.rotate(self.original_image, self.angle+45)
        self.rect = self.image.get_rect(center=self.pos)
    def get_event(self,key):
        speed = 5
        pos = self.rect.topleft
        if key[pg.K_s] and pos[1]+self.rect.height < 1080:
            self.pos[1] +=speed
        if key[pg.K_w] and pos[1] > 0:
            self.pos[1] -=speed
        if key[pg.K_a] and pos[0] > 0:
            self.pos[0]-=speed
        if key[pg.K_d] and pos[0]+self.rect.width <1920:
            self.pos[0]+=speed
    def add_laser(self):
        pg.mixer.music.load('pew.wav')
        pg.mixer.music.play()
        self.lasers.append(Laser(self.rect.center, self.angle))

    def draw(self,surface):
        if self.hp > 0:
            t,r =self.hpdraw()
            self.rotate()
            for x in self.lasers:
                a =x.update(pg.Rect(0,0,19020,1080))
                surface.blit(x.image,x.rect)
                if a:self.lasers.remove(x)
            surface.blit(self.image,self.rect)
            surface.blit(self.a,self.ar)
            a = pg.Surface(((self.hp/self.fullhp)*300,25))
            a.fill(self.color)
            ar = pg.Rect(15,55,(self.hp/self.fullhp)*300,25)
            surface.blit(a,ar)
            surface.blit(t,r)
            return False
        else:
            return True
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
class Enemy(pg.sprite.Sprite):
    def __init__(self,player,pos,*groups):
        super(Enemy,self).__init__(*groups)
        self.pos = pos
        self.player = player
        self.hp = 100
        
        self.fullhp = 100
        self.die = False
        self.sound = pg.mixer.Sound('explode.wav')
        self.original_image = pg.image.load('enemy.png').convert()
        self.original_image.set_colorkey((255,0,255))
        self.image = self.original_image
        self.rect = self.image.get_rect(center = self.pos)
        self.mask = pg.mask.from_surface(self.image)
    def hpdraw(self,screen,c):
        hp = (self.hp/self.fullhp)
        if hp <= 0:
            c.play(self.sound)
            self.die = True
        try:
            x = self.rect.centerx
            y = self.rect.centery-70
            a = pg.Surface((50,14))
            ar = pg.Rect(0,0,50,14)
            ar.center = x,y
            b = pg.Surface((48*hp,10))
            br = pg.Rect(0,0,48*hp,10)
            b.fill((0,255,0))
            br.top = ar.top+1
            br.left = ar.left+1
            screen.blit(a,ar)
            screen.blit(b,br)
        except:
            c.play(self.sound)
            self.die = True
    def hit(self,laser):
        for x in laser:
            if self.rect.colliderect(x.rect):
                self.hp -=10
                x.die()
    def update(self,screen,laser,c,speed):
        self.rotate()
        self.attack(speed)
        self.hit(laser)
        self.hpdraw(screen,c)
    def rotate(self):
        pos = self.player.rect.center
        offset = (pos[1]-self.rect.centery, pos[0]-self.rect.centerx)
        self.angle = 135-math.degrees(math.atan2(*offset))
        self.image = pg.transform.rotate(self.original_image, self.angle+45)
        self.rect = self.image.get_rect(center=self.pos)
    def attack(self,speed):
        speed = 3+speed
        dx,dy = self.rect.x - self.player.rect.x, self.rect.y - self.player.rect.y
        dist = math.hypot(dx,dy)
        if dist !=0:dx,dy = dx/dist,dy/dist
        else:dx,dy = 0,0
        self.pos[0] -= dx*speed
        self.pos[1] -= dy*speed

class Laser(pg.sprite.Sprite):
    def __init__(self,pos, angle, *groups):
        pg.sprite.Sprite.__init__(self,*groups)
        self.original_laser = pg.image.load('laser.png').convert()
        self.original_laser.set_colorkey((255,0,255))
        self.angle = -math.radians(angle-135)
        self.image = pg.transform.rotate(self.original_laser,angle+45)
        self.rect = self.image.get_rect(center =pos)
        self.move = [self.rect.x,self.rect.y]
        self.speed_magnitude = 10
        self.speed = (self.speed_magnitude*math.cos(self.angle),self.speed_magnitude*math.sin(self.angle))
        self.move[0] += self.speed[0]*5
        self.move[1] += self.speed[1]*5
        self.rect.topleft = self.move
        self.kill = False
    def update(self,screen_rect):
        self.move[0] += self.speed[0]
        self.move[1] += self.speed[1]
        self.rect.topleft = self.move
        return self.remove(screen_rect)
    def remove(self,screen_rect):
        if not self.rect.colliderect(screen_rect):
            return True
        if self.kill:
            self.kill = False
            return True
    def die(self):
        self.kill = True

class Game:
    def __init__(self):
        pg.font.init()
        pg.mixer.init()
        self.score = 0
        self.C1 = pg.mixer.Channel(0)
        self.C2 = pg.mixer.Channel(1)
        self.C3 = pg.mixer.Channel(2)
        self.hit = pg.mixer.Sound('hurt.aiff')
        music = pg.mixer.Sound('poppies.wav')
        self.C2.play(music,-1)
        self.screen = pg.display.set_mode((1920,1080),pg.FULLSCREEN)
        self.player = Player()
        self.mouse = Mouse()
        self.enemies = pg.sprite.Group()
        self.add_enemy(random.randint(1,4))
        self.add_enemy(random.randint(1,4))
        self.add_enemy(random.randint(1,4))
        self.done = False
        self.fps = 400.0
        self.a =0
        self.image = pg.image.load('background.jpg').convert_alpha()
        self.clock = pg.time.Clock()
        pg.mouse.set_visible(False)
    def events(self):
        key = pg.key.get_pressed()
        self.player.get_event(key)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.display.update()
                self.done = True
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.player.add_laser()
            
    def check_collide(self):
        if pg.sprite.spritecollide(self.player,self.enemies,False,pg.sprite.collide_mask):
            if self.a%15 == 0:
                self.C3.play(self.hit)
                self.player.hp-=5
            self.a+=1
        else:
            self.a = 0
            pg.display.set_caption(str(round(self.clock.get_fps(),0)))
    def draw_score(self):
        txts = pg.font.SysFont('Courier New', 32).render('score: '+str(self.score), True, (255,255,255))
        txtrect = txts.get_rect()
        txtrect.center = (960,20)
        self.screen.blit(txts,txtrect)
    def draw(self):
        self.screen.fill(BG)
        for y in range(0,1080,168):
            for x in range(0,1920,300):
                self.screen.blit(self.image,(x,y))
        speed = (self.score/30)/5
        for x in self.enemies:
            x.update(self.screen,self.player.lasers,self.C1,speed)
            if x.die == True:
                x.kill()
                self.score+=10
        if self.player.draw(self.screen):
            self.done = True
        self.enemies.draw(self.screen)
        self.mouse.update(self.screen)
        self.draw_score()
    def add_enemy(self,num):
        if num == 1:
            Enemy(self.player,[100,random.randint(100,1070)],self.enemies)
        elif 2:
            Enemy(self.player,[1910,random.randint(100,1070)],self.enemies)
        elif 3:
            Enemy(self.player,[random.randint(100,1910),100],self.enemies)
        elif 4:
            Enemy(self.player,[random.randint(100,1910),1910],self.enemies)
        else:
            print('hm')
    def loop(self):
        while self.done != True:
            self.draw()
            self.events()
            self.check_collide()
            if len(self.enemies) == 0:
                self.add_enemy(random.randint(1,4))
                self.add_enemy(random.randint(1,4))
                self.add_enemy(random.randint(1,4))
            pg.display.update()
            self.clock.tick(self.fps)
        return self.score
