import curses
import time
from view.game_view import GameView
from model.game_model import GameModel

def test_game_view(stdscr):
    stdscr.nodelay(True)  # Make getkey() non-blocking
    max_y, max_x = stdscr.getmaxyx()  # Get the max y and x values

    game_model = GameModel(max_y, max_x)  # Initialize model
    game_view = GameView(game_model, stdscr)  # Initialize view

    game_view.view_reset()  # Render static elements once

    while not game_model.end_game:
        try:
            key = stdscr.getkey()  # Handle input
        except Exception:
            key = ''

        direction = game_model.input_handler(key)
        if direction == "quit":
            break  # Exit the loop if 'quit' command is given
        elif direction:
            game_model.direction = direction

        game_model.update_game()  # Update game state
        game_view.render_game()
        game_view.clear_snake()  # Clear the snake from the screen

      

        stdscr.noutrefresh()  # Efficiently refresh the screen
        curses.doupdate()

        time.sleep(1 / 10)  # Delay for specified time

    game_view.display_end_game_screen()  # Display end game screen
    stdscr.getch()  # Wait for key press to exit

if __name__ == "__main__":
    curses.wrapper(test_game_view)

