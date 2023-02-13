import tkinter as tk
from tkinter import ttk

class Settings:
    def __init__(self, main_canvas: tk.Canvas):
        """
        This class is used to change the settings on-the-fly, without editing the codebase.
        :param main_canvas: The main canvas, in order to apply potential changes in size.
        """
        self.gridSizeX = 5
        self.gridSizeY = 5
        # self.player_nbr = 2
        self.game_mode = 0
        self.main_canvas = main_canvas
        self.window = None
        self.size_x_entry = ttk.Entry()
        self.size_y_entry = ttk.Entry()
        self.game_mode_combo = ttk.Combobox()
        self.players_nbr_entry = ttk.Entry()
        self.player_array = [("Player 1", "blue"), ("Player 2", "red")]
        self.entries = [ttk.Entry()] * (len(self.player_array) * 2)

    def show(self):
        """
        Shows the settings window.
        """
        self.window = tk.Tk()
        self.window.title("Game Settings")
        self.window.geometry("350x450-5+5")
        self.window.resizable(False, True)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        frame = tk.Frame(self.window)
        frame.pack()
        ttk.Label(frame,
                  text="Auto-saves and updates after the window is closed!",
                  font=("Segoe UI", "9", "bold")).grid(row=0, columnspan=2)
        ttk.Label(frame,
                  text="Any incorrect entry will be discarded (at your own risk!).",
                  font=("Segoe UI", "9", "bold")).grid(row=1, columnspan=2)
        ttk.Label(frame,
                  text="You need to restart the game for changes to take effect.",
                  font=("Segoe UI", "9", "bold")).grid(row=2, columnspan=2)
        # TODO: Note to myself: I was too lazy to implement proper input validation using ttk.Entry(validatecommand=)
        # Grid X size setting
        ttk.Label(frame, text="Grid Size X:").grid(row=3)
        self.size_x_entry = ttk.Entry(frame)
        self.size_x_entry.insert(0, str(self.gridSizeX))
        self.size_x_entry.grid(row=3, column=1)
        self.size_x_entry.focus()
        # Grid Y size setting
        ttk.Label(frame, text="Grid Size Y:").grid(row=4)
        self.size_y_entry = ttk.Entry(frame)
        self.size_y_entry.insert(0, str(self.gridSizeY))
        self.size_y_entry.grid(row=4, column=1)
        # Game mode setting
        ttk.Label(frame, text="Game mode:").grid(row=5)
        self.game_mode_combo = ttk.Combobox(frame, values=["Max score mode", "TicTacToe mode"], state="readonly")
        self.game_mode_combo.set(["Max score mode", "TicTacToe mode"][self.game_mode])
        self.game_mode_combo.grid(row=5, column=1)
        ttk.Label(frame,
                  text="Max score: the game continues until the grid is full.",
                  font=("Segoe UI", "9", "italic")).grid(row=6, columnspan=2)
        ttk.Label(frame,
                  text="TicTacToe mode: the first alignment ends the game.",
                  font=("Segoe UI", "9", "italic")).grid(row=7, columnspan=2)
        # Player number settings
        ttk.Label(frame, text="Number of players:").grid(row=8)
        self.players_nbr_entry = ttk.Entry(frame)
        self.players_nbr_entry.insert(0, str(len(self.player_array)))
        self.players_nbr_entry.grid(row=8, column=1)
        # Player settings
        self.entries = [ttk.Entry()] * (len(self.player_array) * 2)
        for i in range(len(self.player_array)):
            ttk.Label(frame, text=f"Player {i + 1}:").grid(row=9+i*3, columnspan=2)
            print(i, self.player_array[i])
            ttk.Label(frame, text="Name:").grid(row=10+i*3)
            self.entries[2*i] = ttk.Entry(frame)
            self.entries[2*i].insert(0, str(self.player_array[i][0]))
            self.entries[2*i].grid(row=10+i*3, column=1)

            ttk.Label(frame, text="Color:").grid(row=11+i*3)
            self.entries[2*i+1] = ttk.Entry(frame)
            self.entries[2*i+1].insert(0, str(self.player_array[i][1]))
            self.entries[2*i+1].grid(row=11+i*3, column=1)

        self.window.mainloop()

    @staticmethod
    def try_parse_int(value: str, minimum: int, maximum: int) -> bool:
        """
        Simple utility method to check if a string can be parsed, and if the int value is bounded.
        :param value: The string to try to parse as an integer.
        :param minimum: The lower bound.
        :param maximum: The upper bound.
        :return: True if the value respects the conditions, False otherwise.
        """
        if value:
            try:
                test = int(value)
                if test < minimum or test > maximum: return False
                return True
            except ValueError:
                return False
        return False

    def on_closing(self):
        """
        This event is fired when the settings window is closed, it is used to save & check the variables.
        :return:
        """
        try:
            # Grid X size setting
            if self.try_parse_int(self.size_x_entry.get(), 3, 15):
                self.gridSizeX = int(self.size_x_entry.get())
            # Grid Y size setting
            if self.try_parse_int(self.size_y_entry.get(), 3, 15):
                self.gridSizeY = int(self.size_y_entry.get())
            # Game mode setting
            self.game_mode = ["Max score mode", "TicTacToe mode"].index(self.game_mode_combo.get())
            # Player number setting
            if self.try_parse_int(self.players_nbr_entry.get(), 2, 10):
                player_nbr = int(self.players_nbr_entry.get())
                # Player settings
                self.player_array = [("Player", "black")] * player_nbr
                for i in range(int(len(self.entries) / 2)):
                    self.player_array[i] = (self.entries[2*i].get(), self.entries[2*i+1].get())
        except Exception as e:
            print("An error was raised while trying to save: ", e)
        finally:
            self.window.destroy()