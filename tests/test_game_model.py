import curses
import time
from view.game_view import GameView
from model.game_model import GameModel  




def test_game_view(stdscr):

    # Get the max y and x values
    max_y, max_x = stdscr.getmaxyx()
    
    # Initialize view and model
    game_model = GameModel(max_y, max_x)
    game_view = GameView(game_model, stdscr)

    # Render static elements (like the box and controls) once at the beginning
    game_view.view_reset()

    while not game_model.end_game:
        # Update then render the game
        game_model.update_game()
        game_view.render_game()

        # Handle input
        try:
            key = stdscr.getkey()
        except Exception:  # No key pressed
            key = ''
        
        direction = game_model.input_handler(key)
        if direction == "quit":
            break  # Exit the loop if 'quit' command is given
        elif direction:
            game_model.direction = direction
        
        # Delay for specified time
        time.sleep(1 / 10)

    # Display end game screen after exiting the loop
    game_view.display_end_game_screen()
    stdscr.getch()  # Wait for key press to exit

if __name__ == "__main__":
    curses.wrapper(test_game_view)

