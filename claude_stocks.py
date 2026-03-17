import tkinter as tk
import random
from datetime import datetime

STOCK_PHRASES = [
    "📈 AAPL — momentum bullish, RSI at 62",
    "💡 Diversification is the only free lunch in investing",
    "📊 S&P 500 holding above 200-day MA — healthy sign",
    "🔍 NVDA riding the AI wave — watch for resistance at ATH",
    "💰 Warren Buffett: 'Be fearful when others are greedy'",
    "📉 Correction incoming? Keep cash ready for opportunities",
    "🌍 DXY rising — pressure on emerging market equities",
    "⚡ TSLA: high beta, not for the faint-hearted",
    "📱 Tech sector P/E elevated — priced for perfection",
    "🏦 Fed holding rates — growth stocks breathe easier",
    "💎 Time in the market beats timing the market",
    "🚀 Small caps lagging large caps — rotation incoming?",
    "📋 Always check the balance sheet before you buy",
    "🎯 SPY bouncing off key support — bulls defending",
    "💼 Risk management > stock picking",
    "📉 VIX spiking — markets pricing in uncertainty",
    "🏆 Compounding works. Start early. Stay patient.",
    "🔮 Earnings season ahead — expect volatility",
    "🛡️ Bonds are back — 5% yield is real competition",
    "🌱 ESG funds underperforming? Market says efficiency wins",
]

AVATARS = ["🤖", "🧑‍💼", "📊", "🤖", "🧑‍💼"]  # cycles for a subtle "blink" feel

class ClaudeStocksPet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Claude")
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.93)

        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()

        self.win_w = 300
        self.win_h = 160

        self.x = float(random.randint(100, self.screen_w - self.win_w - 100))
        self.y = float(random.randint(100, self.screen_h - self.win_h - 200))
        self.target_x = self.x
        self.target_y = self.y

        self.avatar_idx = 0
        self.drag_x = 0
        self.drag_y = 0

        self.setup_ui()
        self.move_tick()
        self.message_tick()
        self.avatar_tick()

    def setup_ui(self):
        self.root.geometry(f"{self.win_w}x{self.win_h}+{int(self.x)}+{int(self.y)}")
        self.root.configure(bg='#0d1117')

        # Outer frame
        outer = tk.Frame(self.root, bg='#161b22', highlightbackground='#30363d',
                         highlightthickness=1)
        outer.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Header row
        header = tk.Frame(outer, bg='#161b22')
        header.pack(fill=tk.X, padx=8, pady=(8, 2))

        self.avatar_lbl = tk.Label(header, text="🤖", font=('Arial', 28),
                                   bg='#161b22')
        self.avatar_lbl.pack(side=tk.LEFT)

        title_frame = tk.Frame(header, bg='#161b22')
        title_frame.pack(side=tk.LEFT, padx=8)

        tk.Label(title_frame, text="Claude", font=('Arial', 12, 'bold'),
                 bg='#161b22', fg='#c9d1d9').pack(anchor='w')
        tk.Label(title_frame, text="Senior Market Analyst", font=('Arial', 8),
                 bg='#161b22', fg='#8b949e').pack(anchor='w')

        # Close button
        tk.Button(header, text="✕", font=('Arial', 8), bg='#161b22',
                  fg='#8b949e', bd=0, cursor='hand2', activebackground='#21262d',
                  activeforeground='#f85149',
                  command=self.root.destroy).pack(side=tk.RIGHT, anchor='n')

        # Divider
        tk.Frame(outer, bg='#30363d', height=1).pack(fill=tk.X, padx=8)

        # Message bubble
        bubble = tk.Frame(outer, bg='#21262d', padx=10, pady=6)
        bubble.pack(fill=tk.X, padx=8, pady=6)

        self.msg_lbl = tk.Label(bubble, text="Analyzing market conditions...",
                                font=('Arial', 9), bg='#21262d', fg='#e6edf3',
                                wraplength=255, justify='left', anchor='w')
        self.msg_lbl.pack(fill=tk.X)

        # Footer
        footer = tk.Frame(outer, bg='#161b22')
        footer.pack(fill=tk.X, padx=8, pady=(0, 6))

        self.time_lbl = tk.Label(footer, text="", font=('Arial', 7),
                                 bg='#161b22', fg='#484f58')
        self.time_lbl.pack(side=tk.LEFT)

        self.dot_lbl = tk.Label(footer, text="● LIVE", font=('Arial', 7),
                                bg='#161b22', fg='#3fb950')
        self.dot_lbl.pack(side=tk.RIGHT)

        # Drag bindings
        for widget in [outer, header, bubble, footer, self.msg_lbl,
                        self.avatar_lbl, self.time_lbl]:
            widget.bind('<Button-1>', self.start_drag)
            widget.bind('<B1-Motion>', self.on_drag)

    def start_drag(self, e):
        self.drag_x = e.x_root - self.x
        self.drag_y = e.y_root - self.y

    def on_drag(self, e):
        self.x = e.x_root - self.drag_x
        self.y = e.y_root - self.drag_y
        self.target_x = self.x
        self.target_y = self.y
        self.root.geometry(f"+{int(self.x)}+{int(self.y)}")

    def move_tick(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        speed = 0.018

        self.x += dx * speed
        self.y += dy * speed

        if abs(dx) < 3 and abs(dy) < 3:
            self.pick_new_target()

        self.x = max(0, min(self.x, self.screen_w - self.win_w))
        self.y = max(0, min(self.y, self.screen_h - self.win_h))

        self.root.geometry(f"+{int(self.x)}+{int(self.y)}")
        self.root.after(40, self.move_tick)

    def pick_new_target(self):
        # Stay in roughly same quadrant most of the time, occasionally wander
        if random.random() < 0.15:
            self.target_x = random.randint(30, self.screen_w - self.win_w - 30)
            self.target_y = random.randint(30, self.screen_h - self.win_h - 80)
        else:
            cx = int(self.x)
            cy = int(self.y)
            margin = 180
            self.target_x = max(30, min(self.screen_w - self.win_w - 30,
                                        cx + random.randint(-margin, margin)))
            self.target_y = max(30, min(self.screen_h - self.win_h - 80,
                                        cy + random.randint(-margin, margin)))

    def message_tick(self):
        phrase = random.choice(STOCK_PHRASES)
        self.msg_lbl.config(text=phrase)
        now = datetime.now().strftime("%H:%M:%S")
        self.time_lbl.config(text=now)
        delay = random.randint(4000, 8000)
        self.root.after(delay, self.message_tick)

    def avatar_tick(self):
        # Subtle "expression" change occasionally
        expressions = ["🤖", "🤖", "🤖", "🧐", "🤖", "🤔", "🤖", "😎"]
        self.avatar_lbl.config(text=random.choice(expressions))
        self.root.after(random.randint(3000, 7000), self.avatar_tick)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    pet = ClaudeStocksPet()
    pet.run()
