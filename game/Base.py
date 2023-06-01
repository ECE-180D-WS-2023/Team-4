from GameObject import GameObject
from constants import *
from pygame import mixer

mixer.init()
collision_sound = pygame.mixer.Sound('assets/music/collision.mp3')
collision_sound.set_volume(0.4)

class Base(GameObject):
    def __init__(self, pos, vel, team_num, img="assets/base.png", health=100, shield=0):
        super().__init__((BASE_WIDTH, BASE_HEIGHT), pos, vel, team_num, img, scale= 2.5)
        self.shield = shield
        self.health = health
        self.immune_time = 0

    def draw(self, screen, action=None):
        super().draw(screen, action)

        # Health Bar
        # Advanced Health Bar
        # https://www.youtube.com/watch?v=pUEZbUAMZYA
        pygame.draw.rect(screen, (255,0,0), (self.pos_x - 46.5, self.pos_y - 65, BASE_WIDTH, 12))  # Red
        pygame.draw.rect(screen, (0,128,0), (self.pos_x - 46.5, self.pos_y - 65, BASE_HEIGHT - ((93/20) * (20 - self.health)), 12))  # Green

    def update(self, shots_group, screen):
        shot = pygame.sprite.spritecollideany(self, shots_group)
        if shot:
            if pygame.sprite.spritecollideany(self, shots_group, pygame.sprite.collide_mask):
                collision_sound.play()
                self.health = max(0, self.health-shot.damage)
                shot.kill()

        super().update(screen)
