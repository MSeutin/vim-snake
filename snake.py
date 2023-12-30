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
        self.FRAME_RATE = 5
        self.blue = curses.color_pair(1) | curses.A_BOLD
        self.green = curses.color_pair(2) | curses.A_BOLD
        self.yellow = curses.color_pair(3) | curses.A_BOLD
        self.magenta = curses.color_pair(4) | curses.A_BOLD
        self.cyan = curses.color_pair(5) | curses.A_BOLD
        self.red = curses.color_pair(6) | curses.A_BOLD
        self.initialize_game()

    def initialize_game(self):
        self.stdscr.clear() # clear screen
        self.end_game = False # reset end game flag
        self.score = 0 # reset score
        self.direction = 'right' # reset direction
        self.collision = False # reset collision flag

        self.max_y, self.max_x = self.stdscr.getmaxyx()
        center_y, center_x = self.max_y // 2, self.max_x // 2 # center snake
        self.snake_body = [(center_y, center_x)]
        self.place_food()
        self.stdscr.refresh() # refresh screen to display the messages

    def place_food(self):
        while True:
            # get random x and y coordinates
            y = random.randint(1, self.max_y - 3)
            x = random.randint(1, self.max_x - 3)
            # check if food is not on snake
            if (y,x) != self.snake_body:
                self.food = (y,x)
                # render the food
                self.stdscr.addstr(self.food[0], self.food[1], '🍒', curses.A_BOLD)
                break

    def snake_collision(self):
        head_y, head_x = self.snake_body[0]
        # check if snake collides with itself
        if (head_y, head_x) in self.snake_body[1:]:
            self.collision = True
            return True
        elif head_y == 0 or head_y == self.max_y - 1 or head_x == 0 or head_x == self.max_x - 1:
            self.collision = True
            return True
        else:
            return False

    def input_handler(self, key):
        # Update cursor position based on key press
        if key == 'h' and self.direction != 'right':
            self.direction = 'left'
        elif key == 'j' and self.direction != 'up':
            self.direction = 'down'
        elif key == 'k' and self.direction != 'down':
            self.direction = 'up'
        elif key == 'l' and self.direction != 'left':
            self.direction = 'right'
        elif key == 'q':
            return True
        else:
            return False

    def update_game(self):
        head_y, head_x = self.snake_body[0]
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
        # check if snake head is on food
        if self.snake_body[0] == self.food:
            self.score += 1 # increment score
            self.FRAME_RATE += 1 # increase frame rate
            self.place_food() # place new food
            return True
        
    def render_game(self):
        # Clear snake body
        for y,x in self.snake_body:
            self.stdscr.addstr(y, x, 'X', curses.A_BOLD)
        # Render when food is eaten
        self.stdscr.addstr(self.food[0], self.food[1], '🍒', curses.A_BOLD) 

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
        self.stdscr.addstr(game_over_msg_y, (self.max_x - len(game_over_msg)) // 2, game_over_msg, self.red)
        self.stdscr.addstr(play_again_y, (self.max_x - len(play_again)) // 2, play_again)
        self.stdscr.refresh() # refresh screen to display the messages

        # Wait for 'y' or 'n' key press
        while True:
            response = self.stdscr.getch()
            if response in [ord('y'), ord('Y')]:
                self.end_game = False
                self.collision = False
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
        self.stdscr.addstr(0, score_x_pos, score_text, self.magenta)
        
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
        time.sleep(1 / self.FRAME_RATE)