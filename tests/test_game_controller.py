import curses
from model.game_model import GameModel
from view.game_view import GameView
from controller.game_controller import GameController

def test_game_controller(stdscr):
    max_y, max_x = stdscr.getmaxyx()

    # Create instances of the model, view, and controller
    game_model = GameModel(max_y, max_x)
    game_view = GameView(game_model, stdscr)
    game_controller = GameController(game_model, game_view)

    # Run the game
    game_controller.run_game()


if __name__ == "__main__":
    curses.wrapper(test_game_controller)

