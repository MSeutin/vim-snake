class GameController:
    """
    A class to control the game's flow in the MVC architecture, handling the interaction 
    between the model and the view.

    Attributes:
        model (GameModel): The game's model, managing the game's data and logic.
        view (GameView): The game's view, responsible for rendering the graphical output.
        timeout (int): The timeout value for the game loop, controlling the game's speed.

    Methods:
        init_game(): Initializes the game's view and model.
        update_game_speed(): Increases the game speed by decreasing the timeout.
        run_game(): The main game loop, handling the game's updates, rendering, and user input.
    """
    def __init__(self, model, view):
        """
        Initializes the GameController with the provided model and view.

        Args:
            model (GameModel): An instance of the game's model.
            view (GameView): An instance of the game's view.
        """
        self.model = model
        self.view = view
        self.timeout = 100
        self.init_game()

    def init_game(self):
        """
        Initializes the game by setting up the view and resetting the model. 
        Also sets the initial timeout for the game loop.
        """
        self.view.create_window()
        self.view.view_reset()
        self.view.window.timeout(self.timeout)
        self.model.reset_game()

    def update_game_speed(self):
        """
        Updates the game's speed by decreasing the timeout. 
        Ensures that the game does not become excessively fast.
        """
        new_timeout = max(self.timeout - 5, 50)  # Prevents the game from becoming too fast
        self.view.window.timeout(new_timeout)
        self.timeout = new_timeout

    def run_game(self):
        """
        Runs the main game loop. It updates the game state, renders the game,
        and handles user input until the game ends.

        The game loop continues until the user decides to quit or not play again 
        after a game over. Also handles the speed increase when the snake eats food.
        """
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

