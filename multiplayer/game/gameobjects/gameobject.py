import pygame

class GameObject:
    frame_width: int
    frame_height: int
    animation_steps: list
    image_path: str
    def __init__(self, pos, vel, direction, scale, animation_cooldown=170, animate=False):
        self.width, self.height = self.frame_width*scale, self.frame_height*scale
        self.rect = pygame.Rect(pos[0] - self.width/2, pos[1] - self.height/2, self.width, self.height)
        self.vel = vel
        self.direction = pygame.math.Vector2(direction)
        self.scale = scale
        self.frame_row, self.frame_col = 0, 0
        self.last_animation_update = pygame.time.get_ticks()
        self.animation_cooldown = animation_cooldown
        self.animate = animate

    @property
    def pos(self):
        return self.rect.centerx, self.rect.centery

    @pos.setter
    def pos(self, pos):
        self.rect.center = pos

    def draw(self, spritesheets, screen, debug=False):
        screen.blit(pygame.transform.scale_by(spritesheets[self.__class__.__name__][self.frame_row][self.frame_col], self.scale), self.rect)
        if debug:
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

    def update(self):
        self.rect.center += self.vel * self.direction

        # Update animation frame
        if self.animate:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_animation_update >= self.animation_cooldown:
                self.frame_col = (self.frame_col + 1) % self.animation_steps[self.frame_row]
                self.last_animation_update = current_time
