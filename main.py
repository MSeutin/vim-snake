import curses
from snake import Snake

def main(stdscr):
    # Start colors in curses
    curses.start_color()
    curses.use_default_colors()
    # Initialize color pairs
    canvas_background = curses.COLOR_WHITE  # You can choose any color
    curses.init_pair(1, curses.COLOR_RED, canvas_background)
    curses.init_pair(2, curses.COLOR_BLUE, canvas_background)
    curses.init_pair(3, curses.COLOR_GREEN, canvas_background)
    curses.init_pair(4, curses.COLOR_YELLOW, canvas_background)
    curses.init_pair(5, curses.COLOR_MAGENTA, canvas_background)
    curses.init_pair(6, curses.COLOR_CYAN, canvas_background)
    curses.init_pair(7, curses.COLOR_WHITE, canvas_background)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(9, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(10, curses.COLOR_BLACK, canvas_background)
    # Set the default background for the stdscr window
    stdscr.bkgd(' ', curses.color_pair(10))

    # Initialize curses
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Make getkey() non-blocking
    stdscr.keypad(True)  # Enable keypad mode to capture arrow keys

    # Declare a snake object
    try:
        snake = Snake(stdscr)
    except Exception:
            # End curses mode and reset terminal to original state
            curses.endwin()
            print('Make your terminal window bigger!')
            input('Press Enter to exit...')
            # Exit the program
            quit()
  
    # Game Loop
    while True:
            
        # Wait for next input
        try:
            key = stdscr.getkey()
        except Exception:
            key = '' 
            
        # Input Handling
        if snake.input_handler(key) or snake.snake_collision():
            snake.display_end_game_screen()
        
        # Break if game over
        if snake.end_game:
                break

        # Update & Render Game
        snake.update_game()
        snake.render_game()
        
        # Refresh only the parts of the screen that have changed
        stdscr.noutrefresh()
        snake.stdscr.noutrefresh()  # snake has its own window 
        curses.doupdate()
        
        # Delay for specified time
        snake.time_delay()
        

if __name__ == '__main__':
    curses.wrapper(main)

### To Dos  ###
# create function comments that can be used in code
# test thoroughly on mac, linux, windows
# unit testing (also make sure size of terminal can fit minimum)
# package into executable and ship and sell online
# Optimize display_end_game_screen Method:

# Improve Readability:
# Adding comments to each method explaining its purpose can greatly improve the readability of your code, especially for others reading it or for yourself when you come back to it later.

# Game Loop Optimization:
# Clearing the screen (stdscr.clear()) and refreshing (stdscr.refresh()) in every iteration could be optimized. Ideally, you should clear and refresh the screen only when there's something new to display. This might require a bit of restructuring in how and when you update the game state and render it.

# Handling Key Presses:
# The try-except block for key presses in the main loop is good, but you might want to handle specific exceptions (like curses.error) instead of a general Exception to avoid catching unintended exceptions.
# Update Method:

# Flesh out the update_game method with the actual game logic. This is where you'll handle things like the movement of the snake, checking for collisions, and updating the game state.

# Add another class for the food object. This will make it easier to handle the food logic separately from the snake logic.

# Add a box around the game area.

# when box is hit, go to display_end_game_screen method

# Add multiple food items

# Maybe add a move vim commands

# test

# package and ship

# post online for $5