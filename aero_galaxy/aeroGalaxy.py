from __future__ import division
import pygame
import random
from os import path

player_dir = path.join(path.dirname(__file__), 'assets/player')
background_dir = path.join(path.dirname(__file__), 'assets/backgrounds')
shoot_dir = path.join(path.dirname(__file__), 'assets/bullets/shoot_sprites')
blast_dir = path.join(path.dirname(__file__), 'assets/bullets/blast_sprites')
explosion_dir = path.join(path.dirname(__file__), 'assets/explosions')
meteor_dir = path.join(path.dirname(__file__), 'assets/meteors')
powerup_dir = path.join(path.dirname(__file__), 'assets/powerups')
sound_folder = path.join(path.dirname(__file__), 'sounds')

WIDTH = 800
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
BAR_LENGTH = 100
BAR_HEIGHT = 10
BACKGROUND_SCROLL_SPEED = 0.5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AERO GALAXY")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('aptos')

def main_menu():
    global screen

    menu_song = pygame.mixer.music.load(path.join(sound_folder, "mmx4-stage-select.ogg"))
    pygame.mixer.music.play(-1)

    title = pygame.image.load(path.join(background_dir, "main.png")).convert()
    title = pygame.transform.scale(title, (WIDTH, HEIGHT), screen)
    
    screen.blit(title, (0,0))
    pygame.display.update()

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break
            elif ev.key == pygame.K_q:
                pygame.quit()
                quit()
        elif ev.type == pygame.QUIT:
                pygame.quit()
                quit() 
        else:
            draw_text(screen, "Press [ENTER] To Begin", 30, WIDTH/2, HEIGHT/2)
            draw_text(screen, "or [Q] To Quit", 30, WIDTH/2, (HEIGHT/2)+40)
            pygame.display.update()

    ready = pygame.mixer.Sound(path.join(sound_folder,'mmx4-ready.ogg'))
    ready.set_volume(0.1)
    ready.play()
    screen.fill(BLACK)
    draw_text(screen, "READY!", 40, WIDTH/2, HEIGHT/2)
    pygame.display.update()    

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_shield_bar(surf, x, y, pct):
    pct = max(pct, 0) 
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect= img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def newmob():
    mob_element = Mob()
    all_sprites.add(mob_element)
    mobs.add(mob_element)

def game_over_screen(score):
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER!", 40, WIDTH / 2, HEIGHT / 3)
    draw_text(screen, f"TOTAL SCORE: {score}", 20, WIDTH / 2, HEIGHT / 2.4)
    draw_text(screen, "PRESS [R] TO RESTART OR [Q] TO QUIT", 30, WIDTH / 2, HEIGHT / 2)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (70, 58))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0 
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()

    def update(self):
        if self.power >=2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 30

        self.speedx = 0
        self.speedy = 0

        keystate = pygame.key.get_pressed()     
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 5

        if keystate[pygame.K_UP]:
            self.speedy = -5
        elif keystate[pygame.K_DOWN]:
            self.speedy = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Shoot(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shooting_sound.play()
            if self.power == 2:
                bullet1 = Shoot(self.rect.left, self.rect.centery)
                bullet2 = Shoot(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shooting_sound.play()

            if self.power >= 3:
                bullet1 = Shoot(self.rect.left, self.rect.centery)
                bullet2 = Shoot(self.rect.right, self.rect.centery)
                missile1 = Blast(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(missile1)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(missile1)
                shooting_sound.play()
                missile_sound.play()

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.90 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(5, 40)
        self.speedx = random.randrange(-3, 6)
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks() 

    def rotate(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update > 50:
            self.last_update = time_now
            self.rotation = (self.rotation + self.rotation_speed) % 360 
            new_image = pygame.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()
            
class Shoot(pygame.sprite.Sprite):
    shoot_images = []
    shoot_list = [
        'shoot1.png',
        'shoot2.png',
        'shoot3.png',
        'shoot4.png',
        'shoot5.png',
        'shoot6.png',
        'shoot7.png',
        'shoot8.png'
    ]
    for simage in shoot_list:
        shoot_images.append(pygame.image.load(path.join(shoot_dir, simage)).convert())

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = Shoot.shoot_images  # Refere-se à variável de classe
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.animation_speed = 3
        self.frame_count = 0

    def update(self):
        self.rect.y += self.speedy

        self.frame_count += 1
        if self.frame_count >= self.animation_speed:
            self.frame_count = 0
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]
            self.image.set_colorkey(BLACK)

        if self.rect.bottom < 0:
            self.kill()

class Blast(pygame.sprite.Sprite):

    blast_images = []
    blast_list = [
        'blast1.png',
        'blast2.png',
        'blast3.png',
        'blast4.png',
        'blast5.png',
        'blast6.png',
    ]
    for blastimage in blast_list:
        blast_images.append(pygame.image.load(path.join(blast_dir, blastimage)).convert())

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = Blast.blast_images
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.animation_speed = 3
        self.frame_count = 0

    def update(self):
        self.rect.y += self.speedy
        
        self.frame_count += 1
        if self.frame_count >= self.animation_speed:
            self.frame_count = 0
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]
            self.image.set_colorkey(BLACK)

        if self.rect.bottom < 0:
            self.kill()


background = pygame.image.load(path.join(background_dir, 'bg.png')).convert()
background = pygame.transform.scale(background, (WIDTH, 1200))
background_rect = background.get_rect()
background_y = 0

player_img = pygame.image.load(path.join(player_dir, 'spaceship.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)

meteor_images = []
meteor_list = [
    'meteorBrown_big1.png',
    'meteorBrown_big2.png', 
    'meteorBrown_med1.png', 
    'meteorBrown_med3.png',
    'meteorBrown_small1.png',
    'meteorBrown_small2.png',
    'meteorBrown_tiny1.png'
]

for image in meteor_list:
    meteor_images.append(pygame.image.load(path.join(meteor_dir, image)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []

for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(explosion_dir, filename)).convert()
    img.set_colorkey(BLACK)

    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(explosion_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(powerup_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(powerup_dir, 'bolt_gold.png')).convert()

shooting_sound = pygame.mixer.Sound(path.join(sound_folder, 'mmx4-shot.ogg'))
shooting_sound.set_volume(0.1)

missile_sound = pygame.mixer.Sound(path.join(sound_folder, 'mmx4-blast.wav'))
missile_sound.set_volume(0.1)

expl_sounds = []
for sound in ['expl1.wav', 'expl2.wav']:
    sound_obj = pygame.mixer.Sound(path.join(sound_folder, sound))
    sound_obj.set_volume(0.1)
    expl_sounds.append(sound_obj)
pygame.mixer.music.set_volume(0.1)

player_die_sound = pygame.mixer.Sound(path.join(sound_folder, 'mmx4-zero-die.ogg'))
player_die_sound.set_volume(0.2)

running = True
menu_display = True
while running:
    if menu_display:
        main_menu()
        pygame.time.wait(3000)

        pygame.mixer.music.stop()

        pygame.mixer.music.load(path.join(sound_folder, 'mmx4-cyberpeacock-theme.ogg'))
        pygame.mixer.music.play(-1) 
        pygame.mixer.music.set_volume(0.2)
        
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        mobs = pygame.sprite.Group()
        for i in range(8):
            newmob()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()

        score = 0
        menu_display = False
        
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    background_y += 0.5
    if background_y >= 600:
        background_y = 0

    screen.fill(BLACK)
    screen.blit(background, (0, background_y - 600))
    screen.blit(background, (0, background_y))
    
    all_sprites.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 + hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0: 
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()

    if player.lives == 0 and not death_explosion.alive():
        game_over_screen(score)
        menu_display = True

    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)

    pygame.display.flip()       

pygame.quit()
