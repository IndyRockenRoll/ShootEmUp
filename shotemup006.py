import pygame
import random

import os

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
FPS = 50

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

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        #self.rect.x = self.rect.x + self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
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

# Load all game sounds
shoot_sound = pygame.mixer.Sound('./shotemup/snd/pew.wav')

# 2 different explosion noises
expl_sounds = []    # this creates an empty list variable called expl_sounds
for snd in ['expl3.wav', 'expl6.wav']:   # this loops twice once with snd = 'expl3.wav' 2nd time 'expl6.wav'
    expl_sounds.append(pygame.mixer.Sound('./shotemup/snd/' + snd)) # adds a new sound object with filename snd to list

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range(8):
    m = Mob()
    mobs.add(m)
    all_sprites.add(m)

score = 0

# Game loop
running = True

while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.shoot()

    # Update
    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)

    if hits:
        running = False

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 30, WIDTH/2, 10)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()