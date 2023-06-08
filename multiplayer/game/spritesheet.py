import pygame

class SpriteSheet():
    def __init__(self, image_surf):
        self.image = image_surf
    
    def get_image(self, sheet_col, sheet_row, width, height, color):
        '''
        frame_col, frame_row: location of a specific frame. frame_col refers to a specific frame of an action. frame_row refers to an action.
        width, height: size of each frame. i.e. 32x32 16x16
        color: get rid of the BG surface color of each frame (transparency color). Usually set to BLACK
        '''
        image = pygame.Surface((width, height))
        image.blit(self.image, (0,0), ((sheet_col * width), (sheet_row * height), width, height))
        # image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)

        return image

    def get_animation_list(self, frame_size, animation_steps=[1], color=(0, 0, 0)):
        '''
        animation_steps: len is number of rows, value of each index is number of col in each row
        '''

        # create animation list
        animation_list = [] # a list of lists. number of lists is number of rows (actions)

        for row in range(len(animation_steps)):
            row_surfaces = []
            for col in range(animation_steps[row]): 
                row_surfaces.append(self.get_image(col, row, frame_size[0], frame_size[1], color))
            animation_list.append(row_surfaces)
        
        return animation_list

class Animation(SpriteSheet):
    def __init__(self, pos, image, animation_steps, frame_size, scale=1, color=(0, 0, 0), animation_cooldown=170, pause_frames=[]):
        '''
        image: pygame.image object after calling convert_alpha()
        pause_frame: starting from 0, which frames do you want to pause at
        stop_frame: starting from 0, which frame do you want to stop at

        '''
        super().__init__(image)
        self.image = image
        self.animation_list = self.get_animation_list(frame_size, animation_steps, color)
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = animation_cooldown
        self.frame_row = 0
        self.frame_col = 0
        self.scale = scale
        self.rect = self.animation_list[0][0].get_rect(center=pos)
        self.pause_frames = pause_frames
        self.stopped = False
        self.paused = False

    def draw(self, screen):
        screen.blit(pygame.transform.scale_by(self.animation_list[self.frame_row][self.frame_col], self.scale), self.rect)

    def update(self, loop=False):
        if self.frame_col in self.pause_frames:
            self.paused = True

        if not (self.paused or self.stopped):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update >= self.animation_cooldown:
                self.frame_col = (self.frame_col + 1) % len(self.animation_list[self.frame_row])
                self.last_update = current_time

        if (not loop) and (self.frame_col == len(self.animation_list[self.frame_row]) - 1):
            self.stopped = True
