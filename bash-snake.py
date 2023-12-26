import curses
import time

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
    def initialize_game():
        # set up the game state
        stdscr.clear() # clear screen
        max_y, max_x = stdscr.getmaxyx() # get screen size
        cur_y, cur_x = max_y // 2, max_x // 2 # center initial snake pos
        stdscr.addstr(cur_y, cur_x, ' ', bright_red)  # Draw the cursor in orange
        return cur_x, cur_y
        

    # Input handling Function
    def input_handler(key, cur_x, cur_y, max_x, max_y):
        # Update cursor position based on key press
        if key == 'h' and cur_x > 0:
            cur_x -= 1
        elif key == 'l' and cur_x < max_x - 1:
            cur_x += 1
        elif key == 'j' and cur_y < max_y - 3:
            cur_y += 1
        elif key == 'k' and cur_y > 1:
            cur_y -= 1
        elif key == 'q':  # Quit command
            return cur_x, cur_y, True
        return cur_x, cur_y, False
            

    # Update Function
    def update_game():
        # Update screen
        stdscr.refresh()
        time.sleep(0.1)
        stdscr.clear()
        # move snake
        # check for collisions
        # check and update food
        # return true if game over, else false

    # Render Function
    def render():
        # display snake, food, and score on screen
        pass

    # End game function 
    def end_game():
        # Display game over message
        stdscr.clear()
        game_over_msg = "G A M E  O V E R"
        play_again = "Play Another Game (y / n) ?"

        # Ensure the message positions are within the screen bounds
        max_y, max_x = stdscr.getmaxyx()
        game_over_msg_y = max_y // 2 - 1
        play_again_y = max_y // 2 + 1

        # Print the messages
        stdscr.addstr(game_over_msg_y, (max_x - len(game_over_msg)) // 2, game_over_msg, bright_red)
        stdscr.addstr(play_again_y, (max_x - len(play_again)) // 2, play_again)
        stdscr.refresh() # refresh screen to display the messages

        # Wait for 'y' or 'n' key press
        while True:
            response = stdscr.getch()
            if response in [ord('y'), ord('Y'), ord('n'), ord('N')]:
                return response in [ord('y'), ord('Y')]


    # Outer Loop for the entire program
    while True:
        # variables
        endgame = False
        max_y, max_x = stdscr.getmaxyx() # get window size

        # Call Initialize Game Function
        cur_x, cur_y = initialize_game()

        # Inner Loop - Game Loop
        while not endgame:
            stdscr.addstr(cur_y, cur_x, ' ', bright_red)  # Draw the cursor in orange

            # function call
            update_game()

            # Display Score (top middle) & Game Name (bottom) 
            score = 0
            score_text = f"Score: {score}"
            score_x_pos = max_x // 2 - len(score_text) // 2
            game_name = "V I M  S N A K E"
            game_name_x_pos = max_x // 2 - len(game_name) // 2
            stdscr.addstr(0, score_x_pos, score_text, curses.color_pair(1))  # Display score
            stdscr.addstr(max_y-2, game_name_x_pos, game_name, curses.A_BOLD) # Display game name
        
            # Display controls with keys in red
            controls = [('q', ':Quit'), ('h', ':Left'), ('j', ':Down'),
                    ('k', ':Up'), ('l', ':Right')]
            x = 1
            for key, text in controls:
                stdscr.addstr(max_y - 1, x, key, curses.color_pair(3) | curses.A_BOLD)
                x += len(key)
                stdscr.addstr(max_y - 1, x, text)
                x += len(text) + 2

            try:
                key = stdscr.getkey()
            except Exception:
                key = ''

            # call handle input function
            cur_x, cur_y, quit_game = input_handler(key, cur_x, cur_y, max_x, max_y)

            # check if endgame
            if quit_game:
                endgame = end_game()
                break
        if endgame:
            break
        else:
            initialize_game()


# Run the program
curses.wrapper(main)

### To Dos  ###
# create function comments that can be used in code
# test thoroughly on mac, linux, windows
# unit testing (also make sure size of terminal can fit minimum)
# package into executable and ship and sell online
