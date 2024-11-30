from pygame import *
from random import randint

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 78)

text_win = font2.render('YOU WIN', 1, (0, 200, 0))
text_lost = font2.render('GAME OVER', 1, (200, 0, 0))

img_back = "galaxy.jpg"  
img_hero = "rocket.png" 


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10, 20, 20)
        bullets.add(bullet)


missed = 0


class Enemy(GameSprite):
    def update(self):
        global missed
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            self.rect.y = 2
            self.rect.x = randint(5, win_width - 40)
            self.speed = randint(1, 5)
            missed += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player("rocket.png", 5, win_height - 100, 10, 80, 100)

enemy = sprite.Group()
for i in range(5):
    ufo = Enemy("ufo.png", randint(5, win_width - 40), 2, randint(1, 5), 100, 60)
    enemy.add(ufo)

bullets = sprite.Group()

finish = False
clock = time.Clock()
FPS = 60

run = True
score = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        if e.type == KEYDOWN:
            keys = key.get_pressed()
            if keys[K_SPACE]:
                ship.fire()

    if not finish:
        text_lose = font1.render('Alien terlewat:' + str(missed), 1, (245, 132, 132))
        text_score = font1.render('Score:' + str(score), 1, (245, 245, 245))
        window.blit(background, (0, 0))
        window.blit(text_lose, (0, 0))
        window.blit(text_score, (0, 30))

        collides = sprite.groupcollide(enemy, bullets, True, True)

        if collides:
            ufo = Enemy("ufo.png", randint(5, win_width - 40), 2, randint(1, 5), 100, 60)
            enemy.add(ufo)
            score += 1

        if sprite.spritecollide(ship, enemy, False):
            finish = True
            window.blit(text_lost, (200, 240))

        if missed > 10:
            finish = True
            window.blit(text_lost, (200, 240)) 

        ship.update()
        ship.reset()
        enemy.draw(window)
        enemy.update()

        bullets.draw(window)

        if score >= 10:
            finish = True
            window.blit(text_win, (240, 240))

        bullets.update()

        display.update()

    clock.tick(FPS)