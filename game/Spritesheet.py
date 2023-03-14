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

    def get_animation_list(self, animation_steps, frame_size):
        '''
        animation_steps: len is number of rows, value of each index is number of col in each row
        '''

        # create animation list
        animation_list = [] # a list of lists. number of lists is number of rows (actions)

        for row in range(len(animation_steps)):
            temp_img_list = []
            for col in range(animation_steps[row]): 
                temp_img_list.append(self.get_image(col, row, frame_size[0], frame_size[1], 1, BLACK))
            animation_list.append(temp_img_list)
        
        return animation_list
