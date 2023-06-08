import pygame

class _Button:
    def __init__(self, pos, text, text_color=(100,100,100), text_color_hover=(150,150,150), font="assets/fonts/font.ttf", font_size=30):
        self.font = pygame.font.Font(font, font_size)
        self.font_size = font_size
        self.text_surf = self.font.render(text, True, text_color)
        self.text_surf_hover = self.font.render(text, True, text_color_hover)
        self.text_rect = self.text_surf.get_rect(center=pos)
        self.hover_sound = pygame.mixer.Sound('assets/sounds/button_hovering.mp3')
        self.hover_sound.set_volume(0.1)
        self.hover_sound_played = False
        self.press_sound = pygame.mixer.Sound('assets/sounds/button_clicked.mp3')
        self.hover_sound.set_volume(0.7)
        self.pressed = False

    @property
    def is_hovered(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

    def press(self, pos):
        if self.rect.collidepoint(pos):
            self.press_sound.play()
            self.active = True
            return True
        return False

    def draw(self, screen):
        text_surf = self.text_surf_hover if self.is_hovered else self.text_surf
        screen.blit(text_surf, self.text_rect)

    def update(self):
        # Play hover sound
        if self.is_hovered and not self.hover_sound_played:
            self.hover_sound.play()
            self.hover_sound_played = True
        # Unset hover_sound_played when not longer hovering
        elif not self.is_hovered and self.hover_sound_played:
            self.hover_sound_played = False

class ImageButton(_Button):
    def __init__(self, pos, image, hover_image=None, pressed_image=None, text="", font_size=30, text_color=(100,100,100), text_color_hover=(150,150,150)):
        super().__init__(pos, text, font_size=font_size, text_color=text_color, text_color_hover=text_color_hover)
        self.image = image
        self.hover_image = hover_image or image
        self.pressed_image = pressed_image or image
        self.rect = self.image.get_rect(center=pos)

    def draw(self, screen):
        if self.pressed:
            image = self.pressed_image
        elif self.is_hovered:
            image = self.hover_image
        else:
            image = self.image
        screen.blit(image, self.rect)
        super().draw(screen)

class RectButton(_Button):
    def __init__(self, pos, text="", width=650, height=None, fill_color=(201, 187, 159), fill_color_hover=(150,150,150), show_border=True, border_color=(105, 86, 51), border_thickness=6, border_padding=30, border_radius=(35, 10, 10, 35)):
        super().__init__(pos, text)
        self.width = width if width else self.font_size*len(text) + border_padding*2
        self.height = height if height else self.font_size + border_padding*2
        self.rect = pygame.Rect(pos[0] - self.width/2, pos[1] - self.height/2, self.width, self.height)
        self.fill_color = fill_color
        self.fill_color_hover = fill_color_hover
        self.show_border = show_border
        self.border_color = border_color
        self.border_radius = [border_radius for _ in range(4)] if isinstance(border_radius, int) else border_radius
        self.border_thickness = border_thickness
        self.border_padding = border_padding

    def draw(self, screen):
        fill_color = self.fill_color_hover if self.is_hovered else self.fill_color
        pygame.draw.rect(screen, fill_color, self.rect, border_top_left_radius=self.border_radius[0], border_top_right_radius=self.border_radius[1], border_bottom_left_radius=self.border_radius[2], border_bottom_right_radius=self.border_radius[3])  # text box border
        if self.show_border:
            pygame.draw.rect(screen, self.border_color, self.rect, self.border_thickness, border_top_left_radius=self.border_radius[0], border_top_right_radius=self.border_radius[1], border_bottom_left_radius=self.border_radius[2], border_bottom_right_radius=self.border_radius[3])  # text box border
        super().draw(screen)

class TransparentButton(_Button):
    def __init__(self, pos, width, height, text="", debug=False):
        super().__init__(pos, text)
        self.rect = pygame.Rect(pos[0] - width/2, pos[1] - height/2, width, height)
        self.debug = debug

    def draw(self, screen):
        super().draw(screen)
        if self.debug:
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

class ButtonGroup:
    def __init__(self):
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)
        return len(self.buttons) - 1

    def check_for_presses(self, pos):
        for idx, button in enumerate(self.buttons):
            if button.press(pos):
                return idx
        return None

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def update(self):
        for button in self.buttons:
            button.update()
