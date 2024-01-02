import curses
from game_view import GameView

# Mock GameModel for testing
class MockGameModel:
    def __init__(self):
        self.snake_body = [(10, 10), (10, 11), (10, 12)]
        self.food = (5, 5)
        self.score = 0

def test_game_view(stdscr):
    mock_model = MockGameModel()
    game_view = GameView(mock_model, stdscr)

    game_view.view_reset()
    game_view.clear_snake()
    # ... call other methods you want to test ...

    stdscr.getch()  # Wait for a key press to visually inspect the screen

if __name__ == "__main__":
    curses.wrapper(test_game_view)
