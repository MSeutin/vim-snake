import curses
import time

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
        # call the initialize game function
        self.initialize_game()
        # not sure how the game loop will work
        # self.game_loop()

    def initialize_game(self):
        # set up the game state
        self.cur_y, self.cur_x = self.max_y // 2, self.max_x // 2 # center initial snake pos
        self.stdscr.addstr(self.cur_y, self.cur_x, ' ', self.bright_red)  # Draw the cursor in orange
        self.food = [self.cur_y - 3, self.cur_x + 3] 
        self.stdscr.addstr(self.food[0], self.food[1], '@', curses.color_pair(3) | curses.A_BOLD)  # Draw the food in green

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

    def end_game(self):
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
            if response in [ord('y'), ord('Y'), ord('n'), ord('N')]:
                return response in [ord('y'), ord('Y')]

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
        
    def set_end_game(self, end_game):
        self.end_game = end_game
        
    def get_end_game(self):
        return self.end_game
    
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



    # Initialization Function
    # def initialize_game(food, score, max_x, max_y):
    #     # set up the game state
    #     cur_y, cur_x = max_y // 2, max_x // 2 # center initial snake pos
    #     stdscr.addstr(cur_y, cur_x, ' ', bright_red)  # Draw the cursor in orange
    #     food = [cur_y - 3, cur_x + 3] 
    #     stdscr.addstr(food[0], food[1], '@', curses.color_pair(3) | curses.A_BOLD)  # Draw the food in green
    #     return cur_x, cur_y, food
        

    # # Input handling Function
    # def input_handler(key, cur_x, cur_y, max_x, max_y):
    #     # Update cursor position based on key press
    #     if key == 'h' and cur_x > 0:
    #         cur_x -= 1
    #     elif key == 'l' and cur_x < max_x - 1:
    #         cur_x += 1
    #     elif key == 'j' and cur_y < max_y - 3:
    #         cur_y += 1
    #     elif key == 'k' and cur_y > 1:
    #         cur_y -= 1
    #     elif key == 'q':  # Quit command
    #         return cur_x, cur_y, True
    #     return cur_x, cur_y, False
            

    # # Update Function
    # def update_game():
    #     # Update screen
    #     # move snake
    #     # check for collisions
    #     # check and update food
    #     # return true if game over, else false
    #     pass

    # Render Function
    # def render_game(cur_x, cur_y, food, score):
    #     # Render snake
    #     stdscr.addstr(cur_y, cur_x, ' ', bright_red)  # Draw the cursor in orange
    #     # Render food
    #     stdscr.addstr(food[0], food[1], '@', curses.color_pair(3) | curses.A_BOLD)  # Draw in green
    #     # Render screen
    #     # Render score
    #     # Render controls

    # # End game function 
    # def end_game():
    #     # Display game over message
    #     stdscr.clear()
    #     game_over_msg = "G A M E  O V E R"
    #     play_again = "Play Another Game (y / n) ?"

    #     # Ensure the message positions are within the screen bounds
    #     max_y, max_x = stdscr.getmaxyx()
    #     game_over_msg_y = max_y // 2 - 1
    #     play_again_y = max_y // 2 + 1

    #     # Print the messages
    #     stdscr.addstr(game_over_msg_y, (max_x - len(game_over_msg)) // 2, game_over_msg, bright_red)
    #     stdscr.addstr(play_again_y, (max_x - len(play_again)) // 2, play_again)
    #     stdscr.refresh() # refresh screen to display the messages

    #     # Wait for 'y' or 'n' key press
    #     while True:
    #         response = stdscr.getch()
    #         if response in [ord('y'), ord('Y'), ord('n'), ord('N')]:
    #             return response in [ord('y'), ord('Y')]

    # def display_score(score, max_x):
    #     # Display score (top middle)
    #     score_text = f"Score: {score}"
    #     score_x_pos = max_x // 2 - len(score_text) // 2
    #     stdscr.addstr(0, score_x_pos, score_text, curses.color_pair(1))  # Display score
    
    # def display_controls(max_y):
    #     controls = [('q', ':Quit'), ('h', ':Left'), ('j', ':Down'), ('k', ':Up'), ('l', ':Right')]
    #     x = 1
    #     for key, text in controls:
    #         stdscr.addstr(max_y - 1, x, key, curses.color_pair(3) | curses.A_BOLD)
    #         x += len(key)
    #         stdscr.addstr(max_y - 1, x, text)
    #         x += len(text) + 2
    
    # def display_logo(max_x, max_y):
    #     # Display game name (bottom middle)
    #     logo = "S N A K E  G A M E"
    #     logo_x_pos = max_x // 2 - len(logo) // 2
    #     stdscr.addstr(max_y-2, logo_x_pos, logo, curses.A_BOLD)
    
    # Declare a snake object
    snake = Snake(stdscr)

    # Outer Loop for the entire program
    while True:
        # Init
        

        # Call Initialize Game Function
        # cur_x, cur_y, food = initialize_game(food, score, max_x, max_y)
        
        # Initialize game
        snake.initialize_game()

        # Inner Loop - Game Loop
        while not snake.get_end_game():
            # Clear the screen of all previously-printed characters
            stdscr.clear()
             
            # Wait for next input
            try:
                key = stdscr.getkey()
            except Exception:
                key = '' 
                
            # Input Handling
            quit_game = snake.input_handler(key)
            
            # Update Game
            snake.update_game()
            
            # Render Game
            snake.render_game()

            # Function calls
            # cur_x, cur_y, quit_game = input_handler(key, cur_x, cur_y, max_x, max_y)
            # update_game()
            # render_game(cur_x, cur_y, food, score) # Render the game
            
            # Display  Fixed Elements
            snake.display_logo() # display logo
            snake.display_score() # display score
            snake.display_controls() # display controls
            
            # Display  Fixed Elements
            # display_logo(max_x, max_y) # display logo
            # display_score(score, max_x) # display score
            # display_controls(max_y) # display controls        
            
            # Refresh the screen to update its contents
            stdscr.refresh()
            
            # Wait 1/10 of a second before repeating
            snake.time_delay()

            # check if endgame
            if quit_game:
                play_again = snake.end_game()
                if not play_again:
                    snake.set_end_game(True)
                break
        if snake.get_end_game():
            break
        else:
            snake.initialize_game()


# Run the program
curses.wrapper(main)

### To Dos  ###
# create function comments that can be used in code
# test thoroughly on mac, linux, windows
# unit testing (also make sure size of terminal can fit minimum)
# package into executable and ship and sell online
