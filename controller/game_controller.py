class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.timeout = 100
        self.init_game()

    def init_game(self):
        self.view.create_window()
        self.view.view_reset()
        self.view.window.timeout(self.timeout)
        self.model.reset_game()

    def update_game_speed(self):
        new_timeout = max(self.timeout - 5, 50)  # Prevents the game from becoming too fast
        self.view.window.timeout(new_timeout)
        self.timeout = new_timeout

    def run_game(self):
        while True:
            # Update then render the game
            self.model.update_game()
            self.view.render_game()

            # Check if food is eaten and update game speed
            if self.model.food_eaten:
                self.update_game_speed()
                self.model.food_eaten = False

            # Handle input
            key = self.view.window.getch()
            direction = self.model.input_handler(key)
            if direction == "quit" or self.model.end_game:
                user_choice = self.view.display_end_game_screen()
                if user_choice == 'n':
                    break
                self.init_game()  # Resets the game for a new round
            elif direction:
                self.model.direction = direction

        self.view.window.getch()  # Wait for key press to exit

