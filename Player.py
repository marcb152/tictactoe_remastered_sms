class Player:
    def __init__(self, number: int, color: str):
        """
        A simple class to represent a Player object
        :param number: The ID of the player (aka. Player 0, Player 1, and so on...)
        :param color: The color with which the player is represented during the game
        """
        self.id = number
        self.color = color
