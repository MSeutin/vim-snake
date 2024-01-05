import curses
import time
from view.game_view import GameView
from model.game_model import GameModel  


def test_game_view(stdscr):

    # Initialize model and view
    max_y, max_x = stdscr.getmaxyx()
    game_model = GameModel(max_y, max_x)
    game_view = GameView(game_model, stdscr)

    # Set up the view
    game_view.view_reset()

    while True:
        # Update then render the game
        game_model.update_game()
        game_view.render_game()

        # Handle input
        key = game_view.window.getch()  # Using the window for input
        direction = game_model.input_handler(key)
        if direction == "quit":
            game_model.end_game = True
        elif direction:
            game_model.direction = direction

        if game_model.end_game:
            user_choice = game_view.display_end_game_screen()
            if user_choice == 'n':
                break  # Exit the loop if user chooses not to play again
            elif user_choice == 'y':
                game_model.reset_game()
                game_view.view_reset()  # Reset the view for a new game
                continue  # Start a new game loop       

        # Delay for specified time
        time.sleep(1 / 10)

if __name__ == "__main__":
    curses.wrapper(test_game_view)

