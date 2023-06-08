from game.game import Game
from game.scenes.main_menu import *
from game.scenes.splash import *
from game.scenes.play import *
from game.scenes.player_selection import *
from game.scenes.map_selection import *
from game.scenes.host import *
from game.scenes.join import *
from game.scenes.lobby import *
from game.scenes.loading import *
from game.scenes.game import *

def main():
    scenes = {
        "splash": SplashScene(),
        "main_menu": MainMenuScene(),
        "play": PlayScene(),
        "player_selection": PlayerSelectionScene(),
        "map_selection": MapSelectionScene(),
        "host": HostScene(),
        "join": JoinScene(),
        "lobby": LobbyScene(),
        "loading": LoadingScene(),
        "game": GameScene(),
    }
    game = Game(scenes, "splash")
    game.run()

if __name__ == "__main__":
  main()
