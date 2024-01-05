import curses
from view.game_view import GameView

# Mock GameModel for testing
class MockGameModel:
    def __init__(self):
        self.snake_body = [(10, 10), (10, 11), (10, 12)]
        self.food = (5, 5)
        self.score = 0

def test_game_view(stdscr):
    stdscr.nodelay(True)  # Make getkey() non-blocking
    mock_model = MockGameModel()
    game_view = GameView(mock_model, stdscr)
    
    # render static elements
    game_view.view_reset()

    while True:
        # Render dynamic elements
        game_view.render_game()

        # Handle input
        key = stdscr.getch()
        if key == ord('q'):  # Exit on 'q' key
            break
        elif key != -1:
            # Handle other keys if necessary
            pass

        # Efficiently refresh the screen
        stdscr.noutrefresh()
        curses.doupdate()

if __name__ == "__main__":
    curses.wrapper(test_game_view)

