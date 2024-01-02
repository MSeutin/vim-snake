import curses
import time
import random

class GameModel:
    def __init__ (self, stdscr):
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
        self.reset_game()
    
    def reset_game(self):
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
        
    def time_delay(self):
        time.sleep(1 / self.FRAME_RATE)