import time
import tkinter as tk
from tkinter import ttk

# Constants for phase timing
TICK_DURATION = 0.6  # seconds per tick
PHASE_DURATIONS = [
    30 * TICK_DURATION,  # Pre-Clones (30 ticks)
    66 * TICK_DURATION,  # Clones (66 ticks)
    30 * TICK_DURATION,  # Post-Clones (30 ticks)
    60 * TICK_DURATION   # Shield (60 ticks)
]
CYCLE_DURATION = sum(PHASE_DURATIONS)  # Total cycle duration
PHASE_NAMES = ["Pre-Clones", "Clones", "Post-Clones", "Shield"]

# Color Theme (Boss Colors)
BG_COLOR = "#1F1C1C"
BUTTON_COLOR = "#A3640B"
BUTTON_HIGHLIGHT = "#DFA63D"
TEXT_COLOR = "#DFA63D"
TEXT_HIGHLIGHT = "#FFFFFF"
FRAME_COLOR = "#412B18"

class BossPhaseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Eclipse Moon Phases")
        self.root.geometry("500x350")
        self.root.minsize(400, 250)
        self.root.configure(bg=BG_COLOR)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        self.start_time = None  # To store when tracking started
        self.selected_phase = None  # User-selected phase
        
        self.label = tk.Label(root, text="Select the boss's current phase:", fg=TEXT_COLOR, bg=BG_COLOR, font=("Arial", 12, "bold"))
        self.label.grid(row=0, column=0, pady=5, sticky="nsew")
        
        self.phase_buttons = []
        button_frame = tk.Frame(root, bg=FRAME_COLOR)
        button_frame.grid(row=1, column=0, sticky="nsew")
        
        for i, name in enumerate(PHASE_NAMES):
            btn = tk.Button(
                button_frame, text=name, command=lambda i=i: self.set_phase(i),
                font=("Arial", 12, "bold"), bg=BUTTON_COLOR, fg=TEXT_COLOR,
                relief="flat", bd=3, activebackground=BUTTON_HIGHLIGHT,
                highlightthickness=2, padx=10, pady=5
            )
            btn.pack(pady=5, fill='both', expand=True)
            self.phase_buttons.append(btn)
        
        self.phase_display = tk.Label(root, text="Current Phase: N/A", fg=TEXT_COLOR, bg=BG_COLOR, font=("Arial", 14, "bold"))
        self.phase_display.grid(row=2, column=0, pady=10, sticky="nsew")
        
        self.timer_display = tk.Label(root, text="Time Until Next Phase: N/A", fg=TEXT_COLOR, bg=BG_COLOR, font=("Arial", 12, "bold"))
        self.timer_display.grid(row=3, column=0, pady=5, sticky="nsew")
        
        self.always_on_top_var = tk.BooleanVar()
        self.always_on_top_check = ttk.Checkbutton(root, text="Always on Top", variable=self.always_on_top_var, command=self.toggle_always_on_top)
        self.always_on_top_check.grid(row=4, column=0, pady=5, sticky="nsew")
        
        self.update_phase()
    
    def set_phase(self, phase):
        self.selected_phase = phase
        self.start_time = time.time()
        self.update_phase()
    
    def get_current_phase(self):
        if self.start_time is None or self.selected_phase is None:
            return None, None
        
        elapsed_time = (time.time() - self.start_time) % CYCLE_DURATION
        
        total_time = 0
        for i in range(4):
            total_time += PHASE_DURATIONS[i]
            if elapsed_time < total_time:
                time_remaining = total_time - elapsed_time
                return (self.selected_phase + i) % 4, time_remaining
        
        return None, None
    
    def update_phase(self):
        current_phase, time_remaining = self.get_current_phase()
        
        if current_phase is not None:
            self.phase_display.config(text=f"Current Phase: {PHASE_NAMES[current_phase]}")
            self.timer_display.config(text=f"Time Until Next Phase: {time_remaining:.1f} sec")
            
            for i, btn in enumerate(self.phase_buttons):
                btn.config(
                    bg=BUTTON_HIGHLIGHT if i == current_phase else BUTTON_COLOR,
                    fg=TEXT_HIGHLIGHT if i == current_phase else TEXT_COLOR
                )
        
        self.root.after(50, self.update_phase)  # Update every 50ms to stay more accurate
    
    def toggle_always_on_top(self):
        self.root.attributes("-topmost", self.always_on_top_var.get())

if __name__ == "__main__":
    root = tk.Tk()
    app = BossPhaseTracker(root)
    root.mainloop()
