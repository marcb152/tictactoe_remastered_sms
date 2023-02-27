import tkinter as tk

import GameFramework
import Settings

def save():
    """
    Saves everything (mostly).
    """
    settings.save()
    gameInstance.save()

def load():
    """
    Loads all the previously saved data back (if any).
    """
    settings.load()
    gameInstance.load()

if __name__ == '__main__':
    window = tk.Tk()
    window.title("SMS Game")
    window.geometry("-5+5")
    canvas = tk.Canvas(window, bg='white')
    canvas.pack()
    # Sets the focus to listen for key press events
    canvas.focus_set()
    # Initializes the Settings class
    settings = Settings.Settings(canvas)
    # Buttons frame
    frame = tk.Frame(window, height=100)
    frame.pack(side=tk.TOP)
    top_label = tk.Label(frame, text="Players", font=('Helvetica','20','bold'))
    top_label.grid(row=0, columnspan=5, padx=5, pady=5)
    mid_label = tk.Label(frame, text="Score")
    mid_label.grid(row=1, columnspan=5)
    # Initializes the game framework class
    gameInstance = GameFramework.GameFramework(settings, canvas, top_label, mid_label)
    # Buttons
    tk.Button(frame, text='Restart', command=gameInstance.restart).grid(row=2, column=0, padx=5, pady=5)
    tk.Button(frame, text='Settings', command=settings.show).grid(row=2, column=1, padx=5, pady=5)
    tk.Button(frame, text='Save', command=save).grid(row=2, column=2, padx=5, pady=5)
    tk.Button(frame, text='Load', command=load).grid(row=2, column=3, padx=5, pady=5)
    tk.Button(frame, text='Quit', command=window.destroy).grid(row=2, column=4, padx=5, pady=5)

    window.mainloop()