# Music Credit -
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder>
#licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>

import pygame
import random

import os
# this command below can be used to control where your pygame pops up
# last two numbers are x and y position on your windows screen with 0 0 being top left
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50)

currentWorkDir = os.getcwd()
print(currentWorkDir)

#sourceFileDir = os.path.dirname(os.path.abspath(__file__))
#print(sourceFileDir)

#os.chdir(os.path.dirname(os.path.abspath(__file__)))

#currentWorkDir = os.getcwd()
#print(currentWorkDir)

#sourceFileDir = os.path.dirname(os.path.abspath(__file__))
#print(sourceFileDir)

#WIDTH = 480
#HEIGHT = 600
FPS = 100

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
#screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
#(WIDTH, HEIGHT) = pygame.display.get_window_size()
(WIDTH, HEIGHT) = (480,600)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Asteroid Game")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 40:
        pygame.draw.rect(surf, GREEN, fill_rect)
    else:
        pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.rect = self.image.get_rect()
        self.radius = 20
        # don't need this below anymore was just for testing
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250 # this controls the delay between shots if you hold space down
        self.last_shot = pygame.time.get_ticks() # this stores the current elapsed game time in last_shot

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()                  # using the shoot method to handle the shooting with delay logic
        self.rect.x += self.speedx
        #self.rect.x = self.rect.x + self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()                   # rechecks the current elapsed time and stores in now
        if now - self.last_shot > self.shoot_delay:   # only does the shoot action if delay since last is long enough
            self.last_shot = now                       # stores the time of the latest shot so can judge next delay
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((30,40))
        self.image_orig = random.choice(asteroid_images)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width  * 0.85 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3,3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
			# do rotation here
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.x < -25 or self.rect.x > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(1,8)
            self.speedx = random.randrange(-3,3)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

# Load images
background = pygame.image.load('./img/starfield.png')
background_rect = background.get_rect()
player_img = pygame.image.load('./img/playerShip1_orange.png')
bullet_img = pygame.image.load('./img/laserRed16.png')
asteroid_images = []
asteroid_image_files = ['meteorBrown_big1.png', 'meteorBrown_med1.png',
               'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
               'meteorBrown_tiny1.png']
for img in asteroid_image_files:
    asteroid_images.append(pygame.image.load('./img/' + img))

# sets up two lists of images for game explosion animations one large and one small
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load('./img/' + filename)
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)


# Load all game sounds
shoot_sound = pygame.mixer.Sound('./snd/pew.wav')

# 2 different explosion noises
expl_sounds = []    # this creates an empty list variable called expl_sounds
for snd in ['expl3.wav', 'expl6.wav']:   # this loops twice once with snd = 'expl3.wav' 2nd time 'expl6.wav'
    expl_sounds.append(pygame.mixer.Sound('./snd/' + snd)) # adds a new sound object with filename snd to list

# now setup the background music (which will loop endlessly)
pygame.mixer.music.load('./snd/music.ogg')
pygame.mixer.music.set_volume(0.4)



all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range(16):
    m = Mob()
    mobs.add(m)
    all_sprites.add(m)

score = 0
pygame.mixer.music.play(loops=-1) # loops = MINUS 1 means play forever, can also set fixed amt of loops

# Game loop
running = True

not_started = True

while not_started == True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            not_started = False

while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        #elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # no longer needed
        #    player.shoot()                                                 # handled in player object update

    # Update
    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()

        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)

    for hit in hits:
        player.shield -= hit.radius * 2

        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        if player.shield <= 0:
            running = False

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 30, WIDTH/2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
