'''
SpriteSheet class deals with the graphic.png
- get_image: return a specific frame and scale it.
- get_animation_list: return a list of lists. Each inner list contains all the frames of a specific action (walking left, walking up...).
'''

import pygame

BLACK = (0, 0, 0)
class SpriteSheet():
    def __init__(self, image):
        self.sheet = image
    
    def get_image(self, frame_col, frame_row, width, height, scale, color):
        '''
        frame_col, frame_row: location of a specific frame. frame_col refers to a specific frame of an action. frame_row refers to an action.
        width, height: size of each frame. i.e. 32x32 16x16
        color: get rid of the BG surface color of each frame (transparency color). Usually set to BLACK
        '''
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0,0), ((frame_col * width), (frame_row * height), width, height)) # (0,0) is where to load the image, ((frame * width), (level * height), width, height) refers to the location of the frame in the spritesheet
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)

        return image

    def get_animation_list(self, animation_steps, frame_size, scale):
        '''
        animation_steps: len is number of rows, value of each index is number of col in each row
        '''

        # create animation list
        animation_list = [] # a list of lists. number of lists is number of rows (actions)

        for row in range(len(animation_steps)):
            temp_img_list = []
            for col in range(animation_steps[row]): 
                temp_img_list.append(self.get_image(col, row, frame_size[0], frame_size[1], scale, BLACK))
            animation_list.append(temp_img_list)
        
        return animation_list
    

class Animation(SpriteSheet):
    def __init__(self, pos, image, animation_steps, frame_size, scale, animation_cooldown=170, pause=False):
        '''
        image: pygame.image object after calling convert_alpha()

        '''
        self.animation_list = self.get_animation_list(animation_steps, frame_size, scale)
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = animation_cooldown
        self.frame_col = 0
        self.rect = image.get_rect(center=pos)
        self.pause = pause
        super().__init__(image)


    def update(self, screen):
        '''
        blit action on to screen
        

        if self.pause is True, we blit the screen with old frame.
        '''
        if not self.pause:
            self.current_time = pygame.time.get_ticks()
            if self.current_time - self.last_update >= self.animation_cooldown:
                self.frame_col += 1
                self.last_update = self.current_time
                if self.frame_col >= len(self.animation_list[0]):
                    self.frame_col = 0
        screen.blit(self.animation_list[0][self.frame_col], self.rect)