import curses
import time
import random

class GameView:
    def __init__ (self, model, stdscr):
        self.model = model
        self.stdscr = stdscr
        self.max_y, self.max_x = stdscr.getmaxyx()
        self.initialize_ui()
        
    def initialize_ui(self):
        # Start colors in curses
        curses.start_color()
        curses.use_default_colors()
        # Initialize color pairs
        canvas_background = curses.COLOR_WHITE 
        # Define color pairs
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
        # Assigning color pairs to variables
        self.red = curses.color_pair(1)
        self.blue = curses.color_pair(2)
        self.green = curses.color_pair(3)
        self.yellow = curses.color_pair(4)
        self.magenta = curses.color_pair(5) | curses.A_BOLD
        self.cyan = curses.color_pair(6)
        self.white = curses.color_pair(7) | curses.A_BOLD
        self.snake_color = curses.color_pair(8) | curses.A_BOLD
        self.food_color = curses.color_pair(9) | curses.A_BOLD
        self.controls_color_reg = curses.color_pair(10)
        self.controls_color_bold = curses.color_pair(10) | curses.A_BOLD
        # Set the default background for the stdscr window
        self.stdscr.bkgd(' ', curses.color_pair(10))
      
    def view_reset(self):
        self.stdscr.clear()  # Clear the screen
        self.stdscr.box()    # Draw the game border
        self.display_fixed_elements()
        self.stdscr.refresh() 

    def clear_snake(self):
        # Iterate over the snake's body except the head
        for y, x in self.model.snake_body:
            try:
                self.stdscr.addstr(y, x, ' ')
            except curses.error:
                pass # Ignore error when snake is out of bounds
            
        # Clear previous food position
        if self.model.food: # Check if food position is defined
            try:
                self.stdscr.addstr(self.model.food[0], self.model.food[1], ' ')
            except curses.error:
                pass # Ignore error when food is out of bounds
    
    def display_end_game_screen(self):
        # Display game over message
        self.stdscr.clear()
        game_over_msg = "G A M E  O V E R"
        play_again = "Play Another Game (y / n) ?"
        score = f"YOUR SCORE: {self.model.score}"

        # Ensure the message positions are within the screen bounds
        self.max_y, self.max_x = self.stdscr.getmaxyx()
        game_over_msg_y = self.max_y // 2 - 1
        play_again_y = self.max_y // 2 + 1
        score_y = 2

        # Print the messages
        self.stdscr.addstr(score_y, (self.max_x - len(score)) // 2, score, self.blue)
        self.stdscr.addstr(game_over_msg_y, (self.max_x - len(game_over_msg)) // 2, game_over_msg, self.red)
        self.stdscr.addstr(play_again_y, (self.max_x - len(play_again)) // 2, play_again)
        
        self.display_logo()
        self.stdscr.refresh() # refresh screen to display the messages

    def display_fixed_elements(self):
        # self.display_logo()
        self.display_controls()

    def render_score(self):
        # Display score (top middle)
        score_text = f"Score: {self.model.score}"
        score_x_pos = self.max_x // 2 - len(score_text) // 2
        self.stdscr.addstr(0, score_x_pos, score_text, self.blue)

    def display_controls(self):
        # Define the controls and their descriptions
        # controls = [('[q]', ':Quit'), ('[h]', '\u2190'), ('[j]', '\u2193'), ('[k]', '\u2191'), ('[l]', '\u2192')]
        controls = '  [q]:quit    Vim cmd:  [h] \u2190  [j] \u2193  [k] \u2191  [l] \u2192  '
        
        self.stdscr.addstr(self.max_y - 1, 1, controls, self.controls_color_reg)

    def display_logo(self):
        # Display game name (bottom middle)
        logo = "V I M  S N A K E  G A M E"
        author = "@frenchmike"
        logo_x_pos = self.max_x // 2 - len(logo) // 2
        author_x_pos = self.max_x // 2 - len(author) // 2
        self.stdscr.addstr(self.max_y-5, logo_x_pos, logo, self.cyan)
        self.stdscr.addstr(self.max_y-4, author_x_pos, author, self.cyan)