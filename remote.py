import pygame

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

class Player(object):
    def __init__(self):
        self.player = pygame.rect.Rect((300, 400, 50, 50))
        self.color = "white"

    def move(self, x_speed, y_speed):
        self.player.move_ip((x_speed, y_speed))

    def change_color(self, color):
        self.color= color

    def draw(self, game_screen):
        pygame.draw.rect(game_screen, self.color, self.player)

    pygame.init()

player1 = Player()
player2 = Player()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,600))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.JOYBUTTONDOWN:
            if pygame.joystick.Joystick(1).get_button(0):
                player1.change_color("blue")
            elif pygame.joystick.Joystick(0).get_button(0):
                player2.change_color("red")
        #     elif pygame.joystick.Joystick(1).get_button(0):
        #         player.change_color("green")
        #     elif pygame.joystick.Joystick(1).get_button(1):
        #         player.change_color("purple")

    x1_speed = round(pygame.joystick.Joystick(1).get_axis(0))
    y1_speed = round(pygame.joystick.Joystick(1).get_axis(1))
    x2_speed = round(pygame.joystick.Joystick(0).get_axis(0))
    y2_speed = round(pygame.joystick.Joystick(0).get_axis(1))

    player1.move(x1_speed, y1_speed)
    player2.move(x2_speed, y2_speed)

    screen.fill((0,0,0))
    player1.draw(screen)
    player2.draw(screen)

    pygame.display.update()
    clock.tick(180)


