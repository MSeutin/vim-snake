import curses
import time
import random

class Snake:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.max_y, self.max_x = stdscr.getmaxyx()
        self.cur_y, self.cur_x = self.max_y // 2, self.max_x // 2
        # figure out where to put food
        self.food = [self.cur_y - 3, self.cur_x + 3]
        self.end_game = False
        self.score = 0
        self.FRAME_RATE = 15
        self.FRAME_DELAY = 1 / self.FRAME_RATE
        # not sure the color below is correct
        self.bright_red = curses.color_pair(2) | curses.A_BOLD
        self.initialize_game()

    def initialize_game(self):
        self.stdscr.clear()
        self.max_y, self.max_x = self.stdscr.getmaxyx()
        self.cur_y, self.cur_x = self.max_y // 2, self.max_x // 2 # center initial snake pos
        self.stdscr.addstr(self.cur_y, self.cur_x, ' ', self.bright_red)  # Draw the cursor in orange
        self.food = [self.cur_y - 3, self.cur_x + 3] 
        self.stdscr.addstr(self.food[0], self.food[1], '@', curses.color_pair(3) | curses.A_BOLD) 
        self.stdscr.refresh() # refresh screen to display the messages

    def input_handler(self, key):
        # Update cursor position based on key press
        if key == 'h' and self.cur_x > 0:
            self.cur_x -= 1
        elif key == 'l' and self.cur_x < self.max_x - 1:
            self.cur_x += 1
        elif key == 'j' and self.cur_y < self.max_y - 3:
            self.cur_y += 1
        elif key == 'k' and self.cur_y > 1:
            self.cur_y -= 1
        elif key == 'q':  # Quit command
            return True
        return False
             

    def update_game(self):
        # Update screen
        # move snake
        # check for collisions
        # check and update food
        # return true if game over, else false
        pass

    def render_game(self):
        # Render snake
        self.stdscr.addstr(self.cur_y, self.cur_x, ' ', self.bright_red)  # Draw the cursor in orange
        # Render food
        self.stdscr.addstr(self.food[0], self.food[1], '@', curses.color_pair(3) | curses.A_BOLD) 

    def display_end_game_screen(self):
        # Display game over message
        self.stdscr.clear()
        game_over_msg = "G A M E  O V E R"
        play_again = "Play Another Game (y / n) ?"

        # Ensure the message positions are within the screen bounds
        self.max_y, self.max_x = self.stdscr.getmaxyx()
        game_over_msg_y = self.max_y // 2 - 1
        play_again_y = self.max_y // 2 + 1

        # Print the messages
        self.stdscr.addstr(game_over_msg_y, (self.max_x - len(game_over_msg)) // 2, game_over_msg, self.bright_red)
        self.stdscr.addstr(play_again_y, (self.max_x - len(play_again)) // 2, play_again)
        self.stdscr.refresh() # refresh screen to display the messages

        # Wait for 'y' or 'n' key press
        while True:
            response = self.stdscr.getch()
            if response in [ord('y'), ord('Y')]:
                self.end_game = False
                self.score = 0
                self.initialize_game() # restart game
                break
            elif response in [ord('n'), ord('N')]:
                self.end_game = True
                break

    def display_fixed_elements(self):
        self.display_logo()
        self.display_score()
        self.display_controls()

    def display_score(self):
        # Display score (top middle)
        score_text = f"Score: {self.score}"
        score_x_pos = self.max_x // 2 - len(score_text) // 2
        self.stdscr.addstr(0, score_x_pos, score_text, curses.color_pair(1))
        
    def display_controls(self):
        controls = [('q', ':Quit'), ('h', ':Left'), ('j', ':Down'), ('k', ':Up'), ('l', ':Right')]
        x = 1
        for key, text in controls:
            self.stdscr.addstr(self.max_y - 1, x, key, curses.color_pair(3) | curses.A_BOLD)
            x += len(key)
            self.stdscr.addstr(self.max_y - 1, x, text)
            x += len(text) + 2

    def display_logo(self):
        # Display game name (bottom middle)
        logo = "S N A K E  G A M E"
        logo_x_pos = self.max_x // 2 - len(logo) // 2
        self.stdscr.addstr(self.max_y-2, logo_x_pos, logo, curses.A_BOLD)
    
    def time_delay(self):
        time.sleep(self.FRAME_DELAY)

def main(stdscr):
    # colors 
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Blue text
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_RED)   # Orange text (using red as closest)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Green
    bright_red = curses.color_pair(2) | curses.A_BOLD

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
        


# Run the program
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