#Shmup platform
#Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
#art from Kwnney.nl
import pygame
import random
from os import path
import pprint

WIDTH = 900
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000

#define kolor ijo
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

#set up assets
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, "img")
img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")
pp = pprint.PrettyPrinter(indent=4)

#create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shd_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    bar_Leng = 100
    bar_Heig = 10
    fill = (pct / 100) * bar_Leng
    outline_rect = pygame.Rect(x, y, bar_Leng, bar_Heig)
    fill_rect = pygame.Rect(x, y, fill, bar_Heig)
    pygame.draw.rect(surf, green, fill_rect)
    pygame.draw.rect(surf, white, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_folder, "playerShip1_blue.png")).convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = 25
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.center = (WIDTH / 2, HEIGHT - 50)
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shoot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        js_count = pygame.joystick.get_count()
        if js_count > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

    def update(self):
        # timeout for powerup
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.center = (WIDTH / 2, HEIGHT - 50)
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if player.joystick.get_button(0):
            self.shoot()
        axisA = player.joystick.get_axis(0)
        print(round(axisA))
        if round(axisA) == -1:
            self.speedx = -8

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_snd.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_snd.play()

    def hide(self):
        #:hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

# corona man
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_org = random.choice(meteor_img)
        self.image_org.set_colorkey(black)
        self.image = self.image_org.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        # pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_up = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_up > 50:
            self.last_up = now
            self.rot = (self.rot + self.rot_speed)
            new_image = pygame.transform.rotate(self.image_org, self.rot_speed)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -21)
            self.speedy = random.randrange(1, 10)
            self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(b_img, (12, 36))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -15

    def update(self):
        self.rect.y += self.speedy
        #killer wall
        if self.rect.bottom < 0:
            self.kill()

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_img[self.type]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 4.3

    def update(self):
        self.rect.y += self.speedy
        #killer wall
        if self.rect.bottom > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = expl_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

#load all gane grapics
player_img = pygame.image.load(path.join(img_dir, 'playerShip1_blue.png'))
background = pygame.image.load(path.join(img_dir, "purple.png")).convert()
background_rect = background.get_rect()
b_img = pygame.image.load(path.join(img_dir, "Laser.png")).convert()
player_mi_img = pygame.transform.scale(player_img, (25, 19))
player_mi_img.set_colorkey(black)
meteor_img = []
meteor_list = ["meteorBrown_big4.png", "meteorBrown_big2.png", "meteorBrown_med1.png", "meteorBrown_med3.png",
               "meteorBrown_small1.png", "meteorBrown_small2.png", "meteorBrown_tiny1.png"]

for img in meteor_list:
    meteor_img.append(pygame.image.load(path.join(img_dir, img)).convert())
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    pp.pprint(filename)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    pp.pprint(img)
    img.set_colorkey(black)
    img_lg = pygame.transform.scale(img, (75, 75))
    expl_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    expl_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(black)
    expl_anim['player'].append(img)

powerup_img = {}
powerup_img['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_img['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()

#load all game sound
shoot_snd = pygame.mixer.Sound(path.join(snd_dir, 'Laser_shoot.wav'))
powerup_snd = pygame.mixer.Sound(path.join(snd_dir, 'Awman.wav'))
ex_snd = []
for snd in ['Explosion1.wav', 'Explosion2.wav']:
    ex_snd.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
player_die_snd = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
pygame.mixer.music.load(path.join(snd_dir, 'om_telolet_om.ogg'))
pygame.mixer.music.set_volume(0.6)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
mobs2 = pygame.sprite.Group()
powerups = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(11):
    newmob()
score = 0
pygame.mixer.music.play(loops=-1)
#game loop
running = True
while running:
    #Keep loop running at the right speed
    clock.tick(FPS)

    #Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #joystick code

    #Up to date
    all_sprites.update()

    #hits script(mobs)
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 40 - hit.radius
        random.choice(ex_snd).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    #hits script(player)
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            player_die_snd.play()
            dead_explotion = Explosion(player.rect.center, 'player')
            all_sprites.add(dead_explotion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # check too se if player gaet powerups
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()

    #If player die
    if player.lives == 0 and not dead_explotion.alive():
        running = False

    #Draw / render
    screen.fill(black)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shd_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mi_img)
    # flip the background man
    pygame.display.flip()


pygame.quit()
