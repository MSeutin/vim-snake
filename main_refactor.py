import curses
from game_model import GameModel
from game_view import GameView

def main(stdscr):

    # Initialize curses
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Make getkey() non-blocking
    stdscr.keypad(True)  # Enable keypad mode to capture arrow keys

    # Declare a snake object
    try:
        game_model = GameModel(stdscr)
        game_view = GameView(game_model, stdscr)
    except Exception:
            # End curses mode and reset terminal to original state
            curses.endwin()
            print('Make your terminal window bigger!')
            input('Press Enter to exit...')
            # Exit the program
            quit()

    # Game loop
    while(True):
        game_view.display_end_game_screen()

        response = stdscr.getch()
        if response in [ord('y'), ord('Y')]:
            game_model.reset_game()  # This method resets the game state
            game_view.view_reset()   # Resets the view for a new game
        elif response in [ord('n'), ord('N')]:
            break  # Exit the loop to end the game

if __name__ == '__main__':
    curses.wrapper(main)