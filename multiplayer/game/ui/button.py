import pygame

class Button:
    def __init__(self, pos, text, width=650, height=None, text_color=(123, 103, 65), text_color_hover=(255,255,255), fill_color=(201, 187, 159), fill_color_hover=(150,150,150), show_border=True, border_color=(105, 86, 51), border_thickness=6, border_padding=30, border_radius=(35, 10, 10, 35), font="assets/fonts/font.ttf", font_size=35):
        self.font = pygame.font.Font(font, font_size)
        self.width = width if width else font_size*len(text) + border_padding*2
        self.height = font_size + border_padding*2
        self.text_surf = self.font.render(text, True, text_color)
        self.text_surf_hover = self.font.render(text, True, text_color_hover)
        self.rect = pygame.Rect(pos[0] - self.width/2, pos[1] - self.height/2, self.width, self.height)
        self.text_rect = pygame.Rect(pos[0] - self.text_surf.get_width()/2, pos[1] - self.text_surf.get_height()/2, self.text_surf.get_width(), self.text_surf.get_height())
        self.fill_color = fill_color
        self.fill_color_hover = fill_color_hover
        self.show_border = show_border
        self.border_color = border_color
        self.border_radius = [border_radius for _ in range(4)] if isinstance(border_radius, int) else border_radius
        self.border_thickness = border_thickness
        self.border_padding = border_padding

    @property
    def is_hovered(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

    def press(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False

    def draw(self, screen):
        fill_color = self.fill_color_hover if self.is_hovered else self.fill_color
        pygame.draw.rect(screen, fill_color, self.rect, border_top_left_radius=self.border_radius[0], border_top_right_radius=self.border_radius[1], border_bottom_left_radius=self.border_radius[2], border_bottom_right_radius=self.border_radius[3])  # text box border
        if self.show_border:
            pygame.draw.rect(screen, self.border_color, self.rect, self.border_thickness, border_top_left_radius=self.border_radius[0], border_top_right_radius=self.border_radius[1], border_bottom_left_radius=self.border_radius[2], border_bottom_right_radius=self.border_radius[3])  # text box border
        text_surf = self.text_surf_hover if self.is_hovered else self.text_surf
        screen.blit(text_surf, self.text_rect) # text

    def update(self):
        if self.is_hovered:
            # play hover sound
            ...

class ButtonMenu:
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
            if button.is_hovered:
                button.update()
