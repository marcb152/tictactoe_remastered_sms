class Case:
    def __init__(self, pos_x: int, pos_y: int, instance_id: int):
        """
        The class to represent a case of the game.
        :param pos_x: The X position of the case in the matrix.
        :param pos_y: The Y position of the case in the matrix.
        :param instance_id: The ID of the rectangle linked to it in the canvas.
        """
        self.x = pos_x
        self.y = pos_y
        self.id = instance_id
        self.text_id = -1
        self.text = ""

    def __str__(self):
        return f"{self.text}[Rect_ID: {self.id} | Text_ID: {self.text_id}]({self.x}, {self.y})"

    @staticmethod
    def size() -> int:
        """
        Constant cell size in pixels (there are no Python equivalent to const static properties).
        :return: The value of the cell size.
        """
        return 30
