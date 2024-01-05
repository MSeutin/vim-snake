import random
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP

class GameModel:
    def __init__ (self, max_y, max_x):
        self.max_y = max_y
        self.max_x = max_x
        self.snake_body = []
        self.food = (0,0)
        self.end_game = False
        self.score = 0
        self.direction = 'right'
        self.collision = False
        self.food_eaten = False
        self.reset_game()
    
    def reset_game(self):
        self.end_game = False # reset end game flag
        self.score = 0 # reset score
        self.direction = 'right' # reset direction
        self.collision = False # reset collision flag
        self.food_eaten = False
        self.snake_body = [(self.max_y // 2, self.max_x // 4), (self.max_y // 2, self.max_x // 4 - 1), (self.max_y // 2, self.max_x // 4 - 2)] 
        self.place_food()
        
    def place_food(self):
        while True:
            # get random x and y coordinates
            y = random.randint(2, self.max_y - 3)
            x = random.randint(2, self.max_x - 3)
            # check if food is not on snake
            if (y,x) not in self.snake_body:
                self.food = (y,x)
                break   
    
    def check_food(self):
        near_food = [(self.food[0] + 1, self.food[1]), (self.food[0] - 1, self.food[1]), (self.food[0], self.food[1] + 1), (self.food[0], self.food[1] - 1)]
        # check if snake head is on food
        if self.snake_body[0] in near_food:
            self.place_food() # place new food
            self.score += 1 # increment score
            self.food_eaten = True
            return True
        
    def snake_collision(self):
        head_y, head_x = self.snake_body[0]
        # check if snake collides with itself
        if (head_y, head_x) in self.snake_body[1:]:
            print("ERROR IMMEDIATE COLLISION")
            self.collision = True
            return True
        if head_y <= 1 or head_y >= self.max_y - 1 or head_x <= 1 or head_x >= self.max_x - 1:
            self.collision = True
            return True
        else:
            return False
    
    def input_handler(self, key):
        # Update cursor position based on key press
        if (key == ord('h') or key == KEY_LEFT) and self.direction != 'right':
            return 'left'
        elif (key == ord('j') or key == KEY_DOWN) and self.direction != 'up':
            return 'down'
        elif (key == ord('k') or key == KEY_UP) and self.direction != 'down':
            return 'up'
        elif (key == ord('l') or key == KEY_RIGHT) and self.direction != 'left':
            return 'right'
        elif key == ord('q'):
            return 'quit'
        
    def update_game(self):
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
            self.snake_body.pop()
        if self.snake_collision():
            self.end_game = True

        
        