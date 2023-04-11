from GameObject import GameObject
from constants import *

class Base(GameObject):
    def __init__(self, pos, vel, team_num, health=100, shield=0):
        super().__init__((BASE_WIDTH, BASE_HEIGHT), pos, vel, team_num, img="assets/base.png")
        self.shield = shield
        self.health = health
        self.immune_time = 0


    def draw(self, screen, action=None):
        if action != None:
            self.frame_row = action

            # Update frame
            self.current_time = pygame.time.get_ticks()
            if self.current_time - self.last_update >= self.animation_cooldown:
                self.frame_col += 1
                self.last_update = self.current_time
                if self.frame_col >= len(self.animation_list[self.frame_row]):
                    self.frame_col = 0

        # Health Bar
        pygame.draw.rect(screen, (255,0,0), (self.pos_x - 46.5, self.pos_y - 65, BASE_WIDTH, 12))  # Red
        pygame.draw.rect(screen, (0,128,0), (self.pos_x - 46.5, self.pos_y - 65, BASE_HEIGHT - ((93/20) * (20 - self.health)), 12))  # Green

        # Draw frame on screen
        screen.blit(self.animation_list[self.frame_row][self.frame_col], self.rect)

