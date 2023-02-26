import tkinter as tk

import Settings
import Case

class GameFramework:
    def __init__(self, settings: Settings, canvas: tk.Canvas, label: tk.Label, score: tk.Label):
        """
        The class which handles the whole game logic.
        :param settings: The settings class, in order to retrieve some useful data.
        :param canvas: The main canvas, to draw on it, kinda useful.
        :param label: The main label used to tell the player's turn & victory.
        """
        self.settings = settings
        self.canvas = canvas
        self.label = label
        self.score = score
        self.cases = []
        self.previous = None
        self.player = 0
        self.scores = [0] * len(self.settings.player_array)
        self.offset = ()
        self.start()
        self.switch_player()

    def start(self):
        """
        This function starts and set-ups the game.
        """
        self.canvas.configure(width=(self.settings.gridSizeX + 3) * Case.Case.size(),
                                   height=(self.settings.gridSizeY + 3) * Case.Case.size())
        self.canvas.bind('<Button-1>', self.select)
        self.canvas.bind('s', lambda event: self.key_press(True))
        self.canvas.bind('m', lambda event: self.key_press(False))
        offset_x = (int(self.canvas.cget("width")) - self.settings.gridSizeX * Case.Case.size()) / 2
        offset_y = (int(self.canvas.cget("height")) - self.settings.gridSizeY * Case.Case.size()) / 2
        self.offset = (int(offset_x), int(offset_y))
        self.cases = [[]] * self.settings.gridSizeY
        for y in range(self.settings.gridSizeY):
            self.cases[y] = [0] * self.settings.gridSizeX
            for x in range(self.settings.gridSizeX):
                rect = self.canvas.create_rectangle(
                    offset_x + x * Case.Case.size(), offset_y + y * Case.Case.size(),
                    offset_x + (x+1) * Case.Case.size(), offset_y + (y+1) * Case.Case.size(),
                    fill="white",
                    outline="black",
                    tags="case")
                self.cases[y][x] = Case.Case(x, y, rect)

    def select(self, event):
        """
        The selection method, event fired on mouse click.
        :param event: The mouse event data
        """
        real_x, real_y = event.x - self.offset[0], event.y - self.offset[1]
        if self.previous: self.canvas.itemconfigure(self.previous.id, outline="black", width=1)
        # Here we check if the mouse click is inside the range of the game
        if (real_x < 0 or real_y < 0
            or real_x > self.settings.gridSizeX * Case.Case.size()
            or real_y > self.settings.gridSizeY * Case.Case.size()):
            return
        # The selection logic
        x, y = real_x // Case.Case.size(), real_y // Case.Case.size()
        # print(f"({x}, {y})")
        self.previous = self.cases[y][x]
        color = self.settings.player_array[self.player][1]
        self.canvas.itemconfigure(self.previous.id, outline=color, width=2)

    def key_press(self, is_key_s: bool):
        """
        Function called after a key is pressed.
        :param is_key_s: Boolean representing which key out of the two is pressed.
        """
        # If no key is selected -> return
        if not self.previous: return
        # We check if the case is empty
        if self.previous.text == "":
            if is_key_s:
                self.previous.text = "S"
            else:
                self.previous.text = "M"
            x, y = self.previous.x, self.previous.y
            self.previous.text_id = self.canvas.create_text(
                self.offset[0] + (x+0.5) * Case.Case.size(),
                self.offset[1] + (y+0.5) * Case.Case.size(),
                text=self.previous.text,
                fill=self.settings.player_array[self.player][1],
                font=('Helvetica','15','bold'),
                tags="case_text")
            self.canvas.itemconfigure(self.previous.id, outline="black", width=1)
            # Checking for end of the game
            has_won = self.check_sms()
            # TicTacToe game mode
            if self.settings.game_mode == 1 and has_won:
                self.end()
                return
            # For both modes, we check if the grid isn't full
            if self.is_grid_full():
                self.end()
                return
            # The game continues
            self.switch_player()

    def switch_player(self):
        """
        This function performs player-switching logic.
        """
        self.player += 1
        if self.player >= len(self.settings.player_array):
            self.player = 0
        (name, color) = self.settings.player_array[self.player]
        self.label.configure(text=name, fg=color)
        self.score.configure(text=f"Score: {self.scores[self.player]}", fg=color)

    def check_sms(self) -> bool:
        """
        This function is vital, it checks for 'SMS' alignments after a new letter is entered.
        :return: True if an alignment was detected, False otherwise.
        """
        interesting_couples = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                # Here we check all the cases surrounding The One, illustration:
                # X X X |
                # X O X | O is the interesting case, aka. The One
                # X X X | X is a checked case
                if i != 0 or j != 0:
                    # print(self.previous, "(", i, ", ", j, ")")
                    case = self.propagate(self.previous, (i, j))
                    # If the case is None, we check the next
                    if not case: continue
                    # If the latest placed text was M
                    if self.previous.text == "M" and case.text == "S":
                        interesting_couples.append((i, j))
                    # If the latest placed text was S
                    if self.previous.text == "S" and case.text == "M":
                        interesting_couples.append((i, j))
        for (i, j) in interesting_couples.copy():
            # If the latest placed text was M
            if self.previous.text == "M":
                if (-i, -j) in interesting_couples:
                    # Player won!
                    interesting_couples.remove((i, j))
                    interesting_couples.remove((-i, -j))
                    self.won(self.propagate(self.previous, (i, j)), self.propagate(self.previous, (-i, -j)))
                    # TicTacToe game mode
                    if self.settings.game_mode == 1:
                        return True
            # If the latest placed text was S
            elif self.previous.text == "S":
                # We continue propagating on the same direction as it looks promising, hehe
                # TODO: improve this chain of functions (Although, I don't care since it will always work)
                last_case = self.propagate(self.propagate(self.previous, (i, j)), (i, j))
                # print("last case: ", last_case, "| (i,j): ", (i,j))
                if last_case and last_case.text == "S":
                    # Player won!
                    interesting_couples.remove((i, j))
                    self.won(self.previous, last_case)
                    # TicTacToe game mode
                    if self.settings.game_mode == 1:
                        return True
        # TODO: Rework the returns to work properly as designed. (Although, I don't care since it will always work)
        return False

    def propagate(self, from_dir: Case, to_dir: (int, int)) -> Case:
        """
        This function checks if a propagation following a vector is possible.
        :param from_dir: The case were the vector starts.
        :param to_dir: The vector.
        :return: Returns the corresponding case if reachable, returns 'None' otherwise.
        """
        (x, y) = to_dir
        if 0 <= from_dir.x + x <= self.settings.gridSizeX - 1:
            if 0 <= from_dir.y + y <= self.settings.gridSizeY - 1:
                return self.cases[from_dir.y + y][from_dir.x + x]
        return None

    def won(self, start_case: Case, end_case: Case):
        """
        This function draws line when an alignment is made.
        :param start_case: One 'S' case of the alignment.
        :param end_case: The second 'S' case of the alignment.
        """
        (name, color) = self.settings.player_array[self.player]
        x0 = self.offset[0] + (start_case.x+0.5) * Case.Case.size()
        y0 = self.offset[1] + (start_case.y+0.5) * Case.Case.size()
        x1 = self.offset[0] + (end_case.x+0.5) * Case.Case.size()
        y1 = self.offset[1] + (end_case.y+0.5) * Case.Case.size()
        self.canvas.create_line(x0, y0, x1, y1, width=2, fill=color, tags="line")
        self.scores[self.player] += 1
        self.score.configure(text=f"Score: {self.scores[self.player]}", fg=color)

    def is_grid_full(self) -> bool:
        """
        Checks if the grid is full or not.
        :return: True is the grid is full, False otherwise.
        """
        for y in range(self.settings.gridSizeY):
            for x in range(self.settings.gridSizeX):
                if self.cases[y][x].text == "":
                    return False
        return True

    def end(self):
        """
        This function ends the game, it can detect if several equally ranked players won.
        """
        # TODO: Test this function (seems to work)
        max_score = max(self.scores)
        # Here we check if two players have the same score or not
        nbr = 0
        for player_score in self.scores:
            if player_score == max_score:
                nbr += 1
        (name, color) = self.settings.player_array[self.scores.index(max_score)]
        if nbr >= 2:
            self.label.configure(text=str(nbr) + " equally ranked players won!", fg=color)
        else:
            self.label.configure(text=name + " won!", fg=color)
        # Show all the players' scores
        sum_scores = ""
        for i in range(len(self.settings.player_array)):
            sum_scores += f"{self.settings.player_array[i][0]}'s score: {self.scores[i]} - "
        sum_scores = sum_scores.rstrip(" - ")
        self.score.configure(text=sum_scores, fg=color)
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('s')
        self.canvas.unbind('m')

    def reset(self):
        """
        This function resets the canvas completely by deleting everything.
        It also resets player scores.
        """
        self.canvas.delete("line")
        self.canvas.delete("case_text")
        self.canvas.delete("case")
        self.scores = [0] * len(self.settings.player_array)

    def restart(self):
        """
        This function restarts the game, whatever state the game was in before.
        """
        self.end()
        self.reset()
        self.start()
        self.switch_player()