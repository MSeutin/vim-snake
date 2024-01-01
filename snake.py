import curses
import time
import random

class Snake:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.max_y, self.max_x = stdscr.getmaxyx()
        self.food = (0,0)
        self.end_game = False
        self.score = 0
        self.snake_body = [(self.max_y // 2, self.max_x // 2)]
        self.direction = 'right'
        self.collision = False
        self.food_eaten = False
        self.food_eaten_time = 0
        self.flash_duration = 0.8
        self.FRAME_RATE = 0
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
        self.initialize_game()

    def initialize_game(self):
        self.stdscr.clear() # clear screen
        self.end_game = False # reset end game flag
        self.score = 0 # reset score
        self.direction = 'right' # reset direction
        self.collision = False # reset collision flag
        self.FRAME_RATE = 15

        self.max_y, self.max_x = self.stdscr.getmaxyx()
        center_y, center_x = self.max_y // 2, self.max_x // 2 # center snake
        self.snake_body = [(center_y, center_x)]
        self.place_food()
        # Draw the static elements once at the beginning
        self.stdscr.box() # draw border
        self.display_fixed_elements()
        self.stdscr.refresh() # refresh screen to display the messages

    def place_food(self):
        while True:
            # get random x and y coordinates
            y = random.randint(2, self.max_y - 3)
            x = random.randint(2, self.max_x - 3)
            # check if food is not on snake
            if (y,x) != self.snake_body:
                self.food = (y,x)
                # render the food
                self.stdscr.addstr(self.food[0], self.food[1], ' ', self.food_color)
                break

    def snake_collision(self):
        head_y, head_x = self.snake_body[0]
        # check if snake collides with itself
        if (head_y, head_x) in self.snake_body[1:]:
            self.collision = True
            return True
        elif head_y <= 1 or head_y >= self.max_y - 1 or head_x <= 1 or head_x >= self.max_x - 1:
            self.collision = True
            return True
        else:
            return False

    def input_handler(self, key):
        # Update cursor position based on key press
        if (key == 'h' or key == 'KEY_LEFT') and self.direction != 'right':
            self.direction = 'left'
        elif (key == 'j' or key == 'KEY_DOWN') and self.direction != 'up':
            self.direction = 'down'
        elif (key == 'k' or key == 'KEY_UP') and self.direction != 'down':
            self.direction = 'up'
        elif (key == 'l' or key == 'KEY_RIGHT') and self.direction != 'left':
            self.direction = 'right'
        elif key == 'q':
            return True
        else:
            return False

    def update_game(self):
        self.clear_snake()
        head_y, head_x = self.snake_body[0]
        new_head = (head_y, head_x)
        # update the current head position based on direction
        if self.direction == 'left':
            new_head = (head_y, head_x - 1)
        elif self.direction == 'right':
            new_head = (head_y, head_x + 1)
        elif self.direction == 'up':
            new_head = (head_y - 1, head_x)
        elif self.direction == 'down':
            new_head = (head_y + 1, head_x)
        # update the snake body
        self.snake_body.insert(0, new_head)
        # check and update food
        if not self.check_food():
            self.snake_body.pop() # remove last segment unless food is eaten
        # return true if game over, else false

    def check_food(self):
        near_food = [(self.food[0] + 1, self.food[1]), (self.food[0] - 1, self.food[1]), (self.food[0], self.food[1] + 1), (self.food[0], self.food[1] - 1)]
        # check if snake head is on food
        if self.snake_body[0] in near_food:
            self.place_food() # place new food
            self.score += 1 # increment score
            self.FRAME_RATE += 1 # increase frame rate
            self.food_eaten = True
            self.food_eaten_time = time.time() # set food eaten time
            return True
        
    def render_game(self):
        current_time = time.time()
        # Clear snake body
        for y, x in self.snake_body:
            if self.food_eaten and current_time - self.food_eaten_time <= self.flash_duration:
                # Flash the head in a different color
                self.stdscr.addstr(y, x, ' ', self.food_color)
            else:
                # Normal rendering
                self.stdscr.addstr(y, x, ' ', self.snake_color)
        # Render when food is eaten
        self.stdscr.addstr(self.food[0], self.food[1], ' ', self.food_color) 
        self.food_eaten = False
        # Render Score
        self.render_score()


    def clear_snake(self):
        # Iterate over the snake's body except the head
        for y, x in self.snake_body:
            self.stdscr.addstr(y, x, ' ')
        # Clear previous food position
        self.stdscr.addstr(self.food[0], self.food[1], ' ')
            
            
    def display_end_game_screen(self):
        # Display game over message
        self.stdscr.clear()
        game_over_msg = "G A M E  O V E R"
        play_again = "Play Another Game (y / n) ?"
        score = f"YOUR SCORE: {self.score}"

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
        
        # refresh screen to display the messages
        self.stdscr.refresh() 

        # Wait for 'y' or 'n' key press
        while True:
            response = self.stdscr.getch()
            if response in [ord('y'), ord('Y')]:
                self.end_game = False
                self.initialize_game() # restart game
                return
            elif response in [ord('n'), ord('N')]:
                self.end_game = True
                return
            


    def display_fixed_elements(self):
        # self.display_logo()
        self.display_controls()

    def render_score(self):
        # Display score (top middle)
        score_text = f"Score: {self.score}"
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
    
    def time_delay(self):
        time.sleep(1 / self.FRAME_RATE)