import tkinter as tk
from PIL import Image, ImageTk
import random
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(SCRIPT_DIR, "claude_logo.png")

class ClaudeFloat:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-transparent', True)
        self.root.configure(bg='systemTransparent')

        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()

        self.size = 80
        self.win_size = self.size + 4

        # Load and resize logo
        img = Image.open(LOGO_PATH).resize((self.size, self.size), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)

        self.canvas = tk.Canvas(self.root, width=self.win_size, height=self.win_size,
                                 bg='systemTransparent', highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_image(self.win_size // 2, self.win_size // 2,
                                  image=self.photo, anchor='center')

        # Position
        self.x = float(random.randint(100, self.screen_w - self.win_size - 100))
        self.y = float(random.randint(100, self.screen_h - self.win_size - 100))
        self.target_x = self.x
        self.target_y = self.y

        # Drag
        self.canvas.bind('<Button-1>', self.start_drag)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<Double-Button-1>', lambda e: self.root.destroy())

        self.root.geometry(f"{self.win_size}x{self.win_size}+{int(self.x)}+{int(self.y)}")
        self.move_tick()

    def start_drag(self, e):
        self.drag_x = e.x_root - self.x
        self.drag_y = e.y_root - self.y

    def on_drag(self, e):
        self.x = e.x_root - self.drag_x
        self.y = e.y_root - self.drag_y
        self.target_x = self.x
        self.target_y = self.y
        self.root.geometry(f"+{int(self.x)}+{int(self.y)}")

    def pick_new_target(self):
        if random.random() < 0.12:
            self.target_x = random.randint(30, self.screen_w - self.win_size - 30)
            self.target_y = random.randint(30, self.screen_h - self.win_size - 80)
        else:
            margin = 200
            self.target_x = max(30, min(self.screen_w - self.win_size - 30,
                                        self.x + random.randint(-margin, margin)))
            self.target_y = max(30, min(self.screen_h - self.win_size - 80,
                                        self.y + random.randint(-margin, margin)))

    def move_tick(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y

        self.x += dx * 0.02
        self.y += dy * 0.02

        if abs(dx) < 3 and abs(dy) < 3:
            self.pick_new_target()

        self.x = max(0, min(self.x, self.screen_w - self.win_size))
        self.y = max(0, min(self.y, self.screen_h - self.win_size))

        self.root.geometry(f"+{int(self.x)}+{int(self.y)}")
        self.root.after(40, self.move_tick)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    ClaudeFloat().run()
