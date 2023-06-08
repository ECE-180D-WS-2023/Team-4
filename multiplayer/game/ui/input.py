import pygame

class InputField:
    def __init__(self, pos, max_chars=15, default_text="", label_text="", label_padding=-2, show_border=True, border_thickness=3, border_padding=5, color=(255,255,255), font_size=75):
        self.font = pygame.font.Font("assets/fonts/bongo.ttf", font_size)
        self.max_chars = max_chars
        self.width = font_size*(max_chars+1) + border_padding*2
        self.height = font_size + border_padding*2
        self.rect = pygame.Rect(pos[0] - self.width/2, pos[1] - self.height/2, self.width, self.height)
        self.text = default_text
        self.label_text = self.font.render(label_text, True, color)
        self.label_padding = label_padding
        self.show_border = show_border
        self.border_thickness = border_thickness
        self.border_padding = border_padding
        self.color = color
        self.active = True
        self.show_cursor = False
        self.cursor_timer = 0

    def process_mousedown(self, event):
        if self.rect.collidepoint(event.pos):
            self.active = True
        else:
            self.active = False
            self.show_cursor = False

    def process_keydown(self, event):
        if event.unicode.isprintable():
            if len(self.text) < self.max_chars:
                self.text += event.unicode
        elif event.key == pygame.K_BACKSPACE:
            self.text = self.text [:-1]

    def draw(self, screen):
        text_surf = self.font.render(self.text, True, self.color)
        screen.blit(text_surf, (self.rect.left + self.border_padding, self.rect.top + self.border_padding)) # text
        if self.show_border:
            pygame.draw.rect(screen, self.color, self.rect, self.border_thickness)  # text box border
        if self.label_text:
            screen.blit(self.label_text, (self.rect.left, (self.rect.top - self.rect.height) - self.label_padding)) # label
        if self.show_cursor:
            screen.blit(self.font.render("|", True, self.color), (self.rect.left + self.border_padding + text_surf.get_width(), self.rect.top + self.border_padding)) # cursor

    def update(self):
        if self.active:
            if pygame.time.get_ticks() - self.cursor_timer > 500:
                self.show_cursor = not self.show_cursor
                self.cursor_timer = pygame.time.get_ticks()
