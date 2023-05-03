import pygame

class SpriteSheet():
    def __init__(self, image_path):
        self.spritesheet = pygame.image.load(image_path).convert_alpha()
    
    def get_image(self, sheet_col, sheet_row, width, height, scale=1, colorkey=(0, 0, 0)):
        '''
        frame_col, frame_row: location of a specific frame. frame_col refers to a specific frame of an action. frame_row refers to an action.
        width, height: size of each frame. i.e. 32x32 16x16
        color: get rid of the BG surface color of each frame (transparency color). Usually set to BLACK
        '''
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.spritesheet, (0,0), ((sheet_col * width), (sheet_row * height), width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colorkey)

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
                temp_img_list.append(self.get_image(col, row, frame_size[0], frame_size[1], scale))
            animation_list.append(temp_img_list)
        
        return animation_list
