from pygame import *
from random import randint
from time import sleep, time as timer

mixer.init()
main_win = display.set_mode((700, 500))
back = transform.scale(image.load('galaxy.jpg') , (700, 500))

mixer.music.load('flower.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.1)

firee = mixer.Sound('fire.ogg')
firee.set_volume(0.1)

score = 0
lost = 0

font.init()
font1 = font.Font(None, 70)
winn = font1.render('YOU WIN!', True, (255, 215, 0))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font.init()
font2 = font.Font(None, 36)

class GameSp(sprite.Sprite):
    def __init__(self, p_image, p_x, p_y, p_speed, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(p_image), (size_x, size_y))
        self.p_speed = p_speed
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y
    def res(self):
        main_win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSp):
    def update(self):
        keypr = key.get_pressed()
        if keypr[K_a] and self.rect.x > 5 or keypr[K_LEFT] and self.rect.y < 630:
            self.rect.x -= self.p_speed
        if keypr[K_d] and self.rect.x < 615 or keypr[K_RIGHT] and self.rect.y < 630:
            self.rect.x += self.p_speed
    def fire(self):
        bullet = Bullet('bullet.png' , gun.rect.x,gun.rect.y, 6, 15,20)
        bullets.add(bullet)


class Enemy(GameSp):
    def update(self):
        self.rect.y += self.p_speed
        global lost
        if self.rect.y > 650:
            self.rect.y = -50
            self.rect.x = randint(0,450)
            lost += 1

class Bullet(GameSp):
    def update(self):
        if self.rect.y < 0:
            self.kill()
        self.rect.y -= self.p_speed

mons = sprite.Group()
for i in range(5):
    mon = Enemy('ufo.png' , randint(0,450),0, randint(1,4), 80,50)
    mons.add(mon)

asts = sprite.Group()
for i in range(3):
    ast = Enemy('asteroid.png' , randint(0,450),0, randint(1,5), 80,50)
    asts.add(ast)

gun = Player('rocket.png' , 350,400, 10, 80,100)

bullets = sprite.Group()

FPS = 60
clock = time.Clock()
game = True
fin = False
num_fire = 7
relo = False
hp_p = 3
while game:
    keys_pr = key.get_pressed()
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if num_fire > 0:
                if i.key == K_SPACE:
                    gun.fire()
                    firee.play()
                    num_fire -= 1
            elif num_fire <= 0 and relo == False:
                relo = True
                last = timer()

    if fin != True:
        main_win.blit(back, (0,0))
        gun.res()
        gun.update()
        mons.update()
        mons.draw(main_win)
        bullets.update()
        bullets.draw(main_win)
        asts.update()
        asts.draw(main_win)

        numa = font2.render('патронов: ' + str(num_fire), 1, (255, 255, 255))
        main_win.blit(numa, (540, 20))

        if relo == True:
            now = timer()
            if now - last < 3:
                wait = font2.render('идет перезарядка..', 1, (255, 255, 255))
                main_win.blit(wait, (225, 350))
            else:
                num_fire = 7
                relo = False

        propuski = font2.render('пропущенно:' + str(lost), 1, (255, 255, 255))
        main_win.blit(propuski, (10, 20))
        ochki = font2.render('счет:' + str(score), 1, (255, 255, 255))
        main_win.blit(ochki, (10, 50))
        cols = sprite.groupcollide(mons, bullets, True, True)

        if sprite.spritecollide(gun, asts, False):
            hp_p -= 1
            sprite.spritecollide(gun, asts, True)

        hp = font2.render('жизней: ' + str(hp_p), 1, (255, 255, 255))
        main_win.blit(hp, (540, 50))

        for i in cols:
            score += 1
            mon = Enemy('ufo.png' , randint(0,450),0, randint(2,4), 80,50)
            mons.add(mon)

        if lost >= 3 or hp_p <= 0:
            sleep(0.01)
            fin = True
            main_win.blit(lose, (200, 200))
        if score >= 10:
            sleep(0.01)
            fin = True
            main_win.blit(winn, (200, 200))

    display.update()
    clock.tick(FPS)


    # sprite.spritecollide(gun, mons, False)