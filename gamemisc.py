import numpy as np
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_RETURN,
    K_SPACE,
    K_ESCAPE,
    K_q,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 20
SLINGSHOT_WIDTH = 50
SLINGSHOT_HEIGHT = 50
SHOT_WIDTH = 5
SHOT_HEIGHT = 10


VEGGIE_POTATO = 5
VEGGIE_CARROT = 7
VEGGIE_CABBAGE = 10
VEGGIE_PUMPKIN = 15

TEAM1 = 1
TEAM2 = 2

all_sprites = pygame.sprite.Group()
shots = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self, x = SCREEN_WIDTH//2, y = SCREEN_HEIGHT//2):
        super(Player, self).__init__()
        self.surf = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.velocity = 5
        self.mounted = False

    def get_position(self):
        return (self.x, self.y)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def move(self, pressed_keys):
        if not self.mounted:
            if pressed_keys[K_UP]:
                self.y -= self.velocity
            if pressed_keys[K_DOWN]:
                self.y += self.velocity
            if pressed_keys[K_LEFT]:
                self.x -= self.velocity
            if pressed_keys[K_RIGHT]:
                self.x += self.velocity

            # TODO: make this actually work
            # Don't allow player to move off screen
            if self.rect.left < 0:
                self.x = PLAYER_WIDTH/2
            if self.rect.right > SCREEN_WIDTH:
                self.x = SCREEN_WIDTH-PLAYER_WIDTH
            if self.rect.top <= 0:
                self.y = PLAYER_HEIGHT
            if self.rect.bottom >= SCREEN_HEIGHT:
                self.y = SCREEN_HEIGHT-PLAYER_HEIGHT

            self.update()

    def update(self):
        self.rect.center = (self.x, self.y)
        
class Slingshot(pygame.sprite.Sprite):
    def __init__(self):
        super(Slingshot, self).__init__()
        self.surf = pygame.Surface((SLINGSHOT_WIDTH, SLINGSHOT_HEIGHT))
        self.surf.fill((175, 175, 175))
        self.rect = self.surf.get_rect(center=(
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT-100
            ))

class Shot(pygame.sprite.Sprite):
    def __init__(self):
        super(Shot, self).__init__()
        self.surf = pygame.Surface((SHOT_WIDTH, SHOT_HEIGHT))
        self.surf.fill((225, 225, 225))
        self.rect = self.surf.get_rect(center=(
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT-100
            ))
        self.speed = 2

    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

def fire_shot():
    shot = Shot()
    shots.add(shot)
    all_sprites.add(shot)

def redraw_screen(screen):
    screen.fill((0, 0, 0))
    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    player = Player()
    slingshot = Slingshot()

    all_sprites.add([player, slingshot])
  
    running = True
    while running:
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_q] or pressed_keys[K_ESCAPE]:
            running = False

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if player.mounted:
                        player.mounted = False
                    elif pygame.sprite.collide_rect(player, slingshot):
                        player.mounted = True
                        player.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT-50)
                elif event.key == K_SPACE:
                    if player.mounted:
                        fire_shot()

        # TODO: export to separate function that creates updates all *local* sprites
        player.update(pressed_keys)
        shots.update()

        redraw_screen()

        # Add collision logic
        if pygame.sprite.spritecollideany(player, shots):
            player.kill()
            running = False

        # Show screen
        pygame.display.flip()

if __name__ == "__main__":
  main()
