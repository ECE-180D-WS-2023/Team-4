'''
SpriteSheet class deals with the graphic.png
- get_image: return a specific frame and scale it.
- get_animation_list: return a list of lists. Each inner list contains all the frames of a specific action (walking left, walking up...).
'''

import pygame
from typing import List, Set, Dict, Tuple

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
    def __init__(self, pos: Tuple[int, int], image, animation_steps, frame_size: Tuple[int, int], scale, animation_cooldown=170, pause_frame=None, stop_frame=None):
        '''
        image: pygame.image object after calling convert_alpha()
        pause_frame: starting from 0, which frames do you want to pause at
        stop_frame: starting from 0, which frame do you want to stop at

        '''
        super().__init__(image)
        self.image = image
        self.animation_list = self.get_animation_list(animation_steps, frame_size, scale)
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = animation_cooldown
        self.frame_col = 0
        self.rect = self.animation_list[0][0].get_rect(center=pos)
        if pause_frame == None:
            self.pause_frame = []
        else:
            self.pause_frame = pause_frame
        if stop_frame == None:
            self.stop_frame = [len(self.animation_list[0]) - 1]
        else:
            self.stop_frame = stop_frame
        self.stop_flag = False
        self.pause_flag = False
    
    def update_norepeat(self, screen, lag=0, resume_signal=False):
        '''
        blit action on to screen
        
        if the current frame is a pause frame;
            1. if there is no resume signal from the main program:
                we continue to update with the old frame
                set the pause_flag
            2. if there is a resume signal:
                we update to the next frame
                set the pause_flag to false and ask the main program to set resume signal to false
        if the current frame is a stop frame:
            1. we update the screen with the last frame
               set the stop_flag
               main program stop execution
        if the current frame is a regular frame:
            update the next frame

        '''  
        # print(self.frame_col)
        if self.frame_col in self.pause_frame:
            self.pause_flag = True
            if resume_signal: # if resume, we increment frame and update screen
                self.pause_flag = False
                self.frame_col += 1
                screen.blit(self.animation_list[0][self.frame_col], self.rect)   # blit the last frame
                return [self.stop_flag, self.pause_flag]
            else: # pause the screen
                screen.blit(self.animation_list[0][self.frame_col], self.rect)   # blit the last frame
                return [self.stop_flag, self.pause_flag]
        elif self.frame_col in self.stop_frame:
            self.stop_flag = True
            screen.blit(self.animation_list[0][self.frame_col], self.rect)   # blit the last frame
            return [self.stop_flag, self.pause_flag]
        else:
            self.current_time = pygame.time.get_ticks()
            if self.current_time - self.last_update >= self.animation_cooldown:
                self.frame_col += 1
                self.last_update = self.current_time
                if self.frame_col >= len(self.animation_list[0]):
                        self.frame_col = 0
            screen.blit(self.animation_list[0][self.frame_col], self.rect)
            return [self.stop_flag, self.pause_flag]


        # self.current_time = pygame.time.get_ticks()
        # if self.current_time - self.last_update >= self.animation_cooldown:
        #     self.frame_col += 1
        #     self.last_update = self.current_time

        #     if self.frame_col in self.stop_frame:
        #         stop_flag = True   # alert main program stop flag
        #         screen.blit(self.animation_list[0][self.frame_col], self.rect)   # blit the previous frame
        #         flags = [stop_flag, pause_flag]
        #         return flags
        #     elif self.frame_col in self.pause_frame :
        #         pause_flag = True
        #         screen.blit(self.animation_list[0][self.frame_col-1], self.rect)

        # if pause_flag:
        #     screen.blit(self.animation_list[0][self.frame_col], self.rect)
        # else:
        #     self.current_time = pygame.time.get_ticks()
        #     if self.current_time - self.last_update >= self.animation_cooldown:
        #         self.frame_col += 1
        #         self.last_update = self.current_time
        #         if self.frame_col == len(self.animation_list[0])-1:
        #             pygame.time.delay(lag)
        #         if self.frame_col >= len(self.animation_list[0]):
        #             stop_flag = True
        #             screen.blit(self.animation_list[0][self.frame_col-1], self.rect)
        #             return stop_flag
        #     screen.blit(self.animation_list[0][self.frame_col], self.rect)
        # return stop_flag

    def repeat(self, screen):
        '''
        Repeatedly blit action on to screen
        

        if self.pause is True, we blit the screen with old frame.
        '''
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_update >= self.animation_cooldown:
            self.frame_col += 1
            self.last_update = self.current_time
            if self.frame_col >= len(self.animation_list[0]):
                    self.frame_col = 0
        screen.blit(self.animation_list[0][self.frame_col], self.rect)