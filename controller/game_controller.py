class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.initial_timeout = 100  # starting timeout in milliseconds
        self.view.window.timeout(self.initial_timeout)
        self.init_game()

    def init_game(self):
        self.view.create_window()
        self.view.view_reset()

    def update_game_speed(self):
        new_timeout = max(self.view.timeout - 5, 50)  # Decrease timeout to increase speed
        self.view.change_timeout(new_timeout)

    def run_game(self):
        while not self.model.end_game:
            # Update then render the game
            self.model.update_game()
            self.view.render_game()

            # Check if food is eaten and update game speed
            if self.model.food_eaten:
                self.update_game_speed()
                self.model.food_eaten = False  # Reset the flag

            # Handle input
            key = self.view.window.getch()
            direction = self.model.input_handler(key)
            if direction == "quit":
                self.model.end_game = True
            elif direction:
                self.model.direction = direction

            if self.model.end_game:
                user_choice = self.view.display_end_game_screen()
                if user_choice == 'n':
                    break
                self.model.reset_game()
                self.view.view_reset()
        self.view.window.getch()  # Wait for key press to exit
