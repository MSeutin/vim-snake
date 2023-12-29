import curses
from snake import Snake

def main(stdscr):
    # colors 
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_RED)  # Blue text
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Green text, black background
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)   # Yellow text, black background
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)   # Magenta text, black background
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Cyan text, black background
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)   # Red text, black background
   

    # Initialize curses
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Make getkey() non-blocking

    # Declare a snake object
    snake = Snake(stdscr)

    # Game Loop
    while True:
        stdscr.clear() # clear screen
            
        # Wait for next input
        try:
            key = stdscr.getkey()
        except Exception:
            key = '' 
            
        # Input Handling
        if snake.input_handler(key):
            snake.display_end_game_screen()
            
        # check end game condition
        if snake.end_game:
            break
        
        # Update & Render Game
        snake.update_game()
        snake.render_game()
        
        # Display Elements
        snake.display_fixed_elements()
        
        # Refresh screen & wait
        stdscr.refresh()
        snake.time_delay()
        

if __name__ == '__main__':
    curses.wrapper(main)

### To Dos  ###
# create function comments that can be used in code
# test thoroughly on mac, linux, windows
# unit testing (also make sure size of terminal can fit minimum)
# package into executable and ship and sell online
# Optimize display_end_game_screen Method:

# After displaying the end game screen and getting the player's response, you could directly handle the restart or termination of the game within this method, rather than using additional checks in the main loop.
# Improve Readability:

# Adding comments to each method explaining its purpose can greatly improve the readability of your code, especially for others reading it or for yourself when you come back to it later.
# Game Loop Optimization:

# Clearing the screen (stdscr.clear()) and refreshing (stdscr.refresh()) in every iteration could be optimized. Ideally, you should clear and refresh the screen only when there's something new to display. This might require a bit of restructuring in how and when you update the game state and render it.
# Handling Key Presses:

# The try-except block for key presses in the main loop is good, but you might want to handle specific exceptions (like curses.error) instead of a general Exception to avoid catching unintended exceptions.
# Update Method:

# Flesh out the update_game method with the actual game logic. This is where you'll handle things like the movement of the snake, checking for collisions, and updating the game state.