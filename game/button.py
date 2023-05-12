import pygame
from pygame import mixer
from Spritesheet import *
from constants import *


mixer.init()
hovering_sound = mixer.Sound('assets/music/button_hovering.mp3')
hovering_sound.set_volume(1.5)

student_select_sound = mixer.Sound('assets/music/Select-sound/student-select-sound.mp3')
student_select_sound.set_volume(0.5)

soldier_select_sound = mixer.Sound('assets/music/Select-sound/soldier-select-sound.mp3')
soldier_select_sound.set_volume(0.5)

enchantress_select_sound = mixer.Sound('assets/music/Select-sound/enchantress-select-sound.mp3')
enchantress_select_sound.set_volume(0.5)
class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color, noise_played=False):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
		self.noise_played = noise_played

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if self.checkForInput(position):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

	def hoverNoise(self, position):
		if self.checkForInput(position):
			if not self.noise_played:
				hovering_sound.play()
				self.noise_played = True	
			else:
				return
		else:
			self.noise_played = False

class PlayerCard(Button):
	def __init__(self, image, pos, text_input, font, base_color, hovering_color, noise_played=False):
		super().__init__(image, pos, text_input, font, base_color, hovering_color, noise_played)
		# Spritesheet and character name text box
		self.sprite_scale = 8
		self.background_scale = 10

		# Surface and rect
		self.surf = pygame.Surface((PLAYER_WIDTH*self.background_scale, PLAYER_HEIGHT*self.background_scale))
		self.surf_img = pygame.image.load('assets/pause-phase/select-surface.png').convert_alpha()
		self.rect = self.surf.get_rect()
		self.rect.center = pos

		# Sprite animation
		self.frame_col = 0
		self.sprite_image=image.convert_alpha()
		self.animation_list = SpriteSheet(self.sprite_image).get_animation_list([3], (PLAYER_WIDTH,PLAYER_HEIGHT), self.sprite_scale)
		self.mask = pygame.mask.from_surface(self.animation_list[0][self.frame_col])
		self.animation_cooldown = 170
		self.last_update = pygame.time.get_ticks()
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos-20))

		# Hovering text box
		self.hoverbox_width = 500
		self.hoverbox_height = 1000
		self.hoverbox_surf = pygame.Surface((self.hoverbox_width, self.hoverbox_height))
		self.hoverbox_surf.fill((255,255,255))
	
	def update(self, screen):
		# Sprite animation
		self.current_time = pygame.time.get_ticks()
		if self.current_time - self.last_update >= self.animation_cooldown:
			self.frame_col += 1
			self.last_update = self.current_time
			if self.frame_col >= len(self.animation_list[0]):
				self.frame_col = 0

		# Background
		screen.blit(self.surf_img, self.rect)

		# Animation
		screen.blit(self.animation_list[0][self.frame_col], self.rect)
		screen.blit(self.text, self.text_rect)
		self.mask = pygame.mask.from_surface(self.animation_list[0][self.frame_col])

class StudentCard(PlayerCard):
	def __init__(self, image, pos, text_input, font, base_color, hovering_color, noise_played=False):
		super().__init__(image, pos, text_input, font, base_color, hovering_color, noise_played)
	

	def hoverNoise(self, position):
		if self.checkForInput(position):
			if not self.noise_played:
				student_select_sound.play()
				self.noise_played = True	
			else:
				return
		else:
			self.noise_played = False

	def hoverShow(self, position, screen):
		if self.checkForInput(position):
			text = "Student -> Engineer\n Student:\n Health: 100 \n Engineer: \n Health: 100"
			self.hoverbox_pos = (position[0]+10, position[1]+10)
			self.text_surf = self.font.render(text, True, (0,0,0))
			text_pos = ((self.hoverbox_width - self.text_surf.get_width()) //2, (self.hoverbox_height - self.text_surf.get_height()) // 2)
			self.hoverbox_surf.blit(self.text_surf, text_pos)
			screen.blit(self.hoverbox_surf, self.hoverbox_pos)

class SoldierCard(PlayerCard):
	def __init__(self, image, pos, text_input, font, base_color, hovering_color, noise_played=False):
		super().__init__(image, pos, text_input, font, base_color, hovering_color, noise_played)
	

	def hoverNoise(self, position):
		if self.checkForInput(position):
			if not self.noise_played:
				soldier_select_sound.play()
				self.noise_played = True	
			else:
				return
		else:
			self.noise_played = False

	def hoverShow(self, position, screen):
		if self.checkForInput(position):
			text = "Student -> Engineer\n Student:\n Health: 100 \n Engineer: \n Health: 100"
			self.hoverbox_pos = (position[0]+10, position[1]+10)
			self.text_surf = self.font.render(text, True, (0,0,0))
			text_pos = ((self.hoverbox_width - self.text_surf.get_width()) //2, (self.hoverbox_height - self.text_surf.get_height()) // 2)
			self.hoverbox_surf.blit(self.text_surf, text_pos)
			screen.blit(self.hoverbox_surf, self.hoverbox_pos)

class EnchantressCard(PlayerCard):
	def __init__(self, image, pos, text_input, font, base_color, hovering_color, noise_played=False):
		super().__init__(image, pos, text_input, font, base_color, hovering_color, noise_played)

	def hoverNoise(self, position):
		if self.checkForInput(position):
			if not self.noise_played:
				enchantress_select_sound.play()
				self.noise_played = True	
			else:
				return
		else:
			self.noise_played = False

	def hoverShow(self, position, screen):
		if self.checkForInput(position):
			text = "Student -> Engineer\n Student:\n Health: 100 \n Engineer: \n Health: 100"
			self.hoverbox_pos = (position[0]+10, position[1]+10)
			self.text_surf = self.font.render(text, True, (0,0,0))
			text_pos = ((self.hoverbox_width - self.text_surf.get_width()) //2, (self.hoverbox_height - self.text_surf.get_height()) // 2)
			self.hoverbox_surf.blit(self.text_surf, text_pos)
			screen.blit(self.hoverbox_surf, self.hoverbox_pos)