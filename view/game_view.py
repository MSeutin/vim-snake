import curses

class GameView:
    def __init__ (self, model, stdscr):
        self.model = model
        self.stdscr = stdscr
        self.create_window()
        self.timeout = 100  # Starting timeout value in milliseconds
        self.window.timeout(self.timeout)
        self.create_window()
        
    def create_window(self):
        self.stdscr.nodelay(True)
        self.max_y, self.max_x = self.stdscr.getmaxyx()
        self.window = curses.newwin(self.max_y, self.max_x, 0, 0)
        self.window.border(0)
        self.window.keypad(True)
        self.window.nodelay(True)
        self.initialize_ui()
        
    def initialize_ui(self):
        try:
            curses.curs_set(0)
        except curses.error:
            pass  # Fails silently if the terminal does not support hiding the cursor
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
        self.window.bkgd(' ', curses.color_pair(10))
      
    def view_reset(self):
        # Initialize static ui elements
        self.window.clear()  # Clear the screen
        self.window.border(0)  # Draw border
        self.render_score()  # Display score
        self.display_controls()
        self.window.refresh() 
        
    def change_timeout(self, new_timeout):
        self.timeout = new_timeout
        self.window.timeout(self.timeout)

    def render_game(self):
        self.window.clear()
        self.window.border(0)
        self.clear_snake() # Clear the snake from the previous frame
        # Render snake
        for segment in self.model.snake_body:
            y, x = segment
            if 0 <= y < self.max_y and 0 <= x < self.max_x:
                try:
                    self.window.addch(y, x, curses.ACS_CKBOARD, self.snake_color)
                except curses.error:
                    pass  # Ignore errors if snake is out of bounds


        # Render food
        if self.model.food:  # Check if food position is defined
            self.window.addch(self.model.food[0], self.model.food[1], curses.ACS_CKBOARD, self.food_color)

        # Render score and controls
        self.render_score()
        self.display_controls()

        # Refresh the screen to display the updates
        self.window.refresh()


    def clear_snake(self):
        # Clear only the last segment of the snake's body
        snake_tail = self.model.snake_body[-1]
        self.window.addch(snake_tail[0], snake_tail[1], ' ')

    def clear_snake(self):
        if not self.model.food_eaten:
            # Clear only the last segment of the snake's body
            snake_tail = self.model.snake_body[-1]
            self.window.addch(snake_tail[0], snake_tail[1], ' ')
            self.model.food_eaten = False  # Reset food eaten flag

        
    
    def display_end_game_screen(self):
        # Display game over message
        self.window.clear()
        game_over_msg = "G A M E  O V E R"
        play_again = "Play Another Game (y / n) ?"
        score = f"YOUR SCORE: {self.model.score}"

        # Ensure the message positions are within the screen bounds
        self.max_y, self.max_x = self.window.getmaxyx()
        game_over_msg_y = self.max_y // 2 - 1
        play_again_y = self.max_y // 2 + 1
        score_y = 2

        # Print the messages
        self.window.addstr(score_y, (self.max_x - len(score)) // 2, score, self.blue)
        self.window.addstr(game_over_msg_y, (self.max_x - len(game_over_msg)) // 2, game_over_msg, self.red)
        self.window.addstr(play_again_y, (self.max_x - len(play_again)) // 2, play_again)
        
        self.display_logo()
        self.window.refresh() # refresh screen to display the messages
        while True:
            response = self.window.getch()
            if response in [ord('y'), ord('Y')]:
                return 'y'
            elif response in [ord('n'), ord('N')]:
                return 'n'

    def render_score(self):
        # Display score (top middle)
        score_text = f"Score: {self.model.score}"
        score_x_pos = self.max_x // 2 - len(score_text) // 2
        self.window.addstr(0, score_x_pos, score_text, self.blue)

    def display_controls(self):
        # Define the controls and their descriptions
        controls = '  [q]:quit    Vim cmd:  [h] \u2190  [j] \u2193  [k] \u2191  [l] \u2192  '
        self.window.addstr(self.max_y - 1, 1, controls, self.controls_color_reg)

    def display_logo(self):
        # Display game name (bottom middle)
        logo = "V I M  S N A K E  G A M E"
        author = "@frenchmike"
        logo_x_pos = self.max_x // 2 - len(logo) // 2
        author_x_pos = self.max_x // 2 - len(author) // 2
        self.window.addstr(self.max_y-5, logo_x_pos, logo, self.cyan)
        self.window.addstr(self.max_y-4, author_x_pos, author, self.cyan)