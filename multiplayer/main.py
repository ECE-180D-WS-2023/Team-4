from game.game import Game
from game.scenes.main_menu import *
from game.scenes.play import *
from game.scenes.host import *
from game.scenes.join import *
from game.scenes.game_host import *
from game.scenes.game_join import *

def main():
    scenes = {
        # "splash": SplashScene(),
        "main_menu": MainMenuScene(),
        "play": PlayScene(),
        "host": HostScene(),
        "join": JoinScene(),
        "game_host": GameHostScene(),
        "game_join": GameJoinScene(),
    }
    game = Game(scenes, "main_menu")
    game.run()

if __name__ == "__main__":
  main()
