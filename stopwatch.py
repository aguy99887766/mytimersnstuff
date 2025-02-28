import tkinter as tk
import time
import menu
class Stopwatch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.start_time = 0
        self.elapsed_time = 0
        self.active = False
        self.elasp = 0
        self.lap_dict = {}
        self.counter = 0

        self.label = tk.Label(self, text="00:00:00")
        self.label.pack(pady=20)

        self.toggle = tk.Button(self, text="Start", command=self.toggle)
        self.toggle.pack(pady=5)

        self.toggle_lap = tk.Button(self, text="Lap", command=self.lap, state=tk.DISABLED)
        self.toggle_lap.pack()

        self.display_laps = tk.Listbox(self)
        self.reset_lap_display()

        self.leave = tk.Button(self, text="Back", command=lambda: controller.show_frame(menu.Start))
        self.leave.pack()
    
    def toggle(self):
        if self.active:
            self.active = False
            self.toggle_lap.config(state=tk.DISABLED)
            self.toggle.config(text="Start")
            self.lap_dict.clear()
            self.counter = 0
            self.reset_lap_display()
        else:
            self.active = True
            self.start_time = time.time() - self.elasp
            self.toggle_lap.config(state=tk.NORMAL)
            self.toggle.config(text="Stop")
            self.update_timer()
            
    def convert_timer(self):
        current_time = time.time() - self.start_time
        self.elapsed_time = current_time
        self.hours, self.rem_seconds = divmod(int(self.elapsed_time), 3600)
        self.minutes, self.seconds = divmod(int(self.rem_seconds), 60)

    def update_timer(self):
        if self.active:
            self.convert_timer()
            self.label.config(text=f"{self.hours:02}:{self.minutes:02}:{self.seconds:02}")
            self.after(1000, self.update_timer) 
        
    def lap(self):
        self.convert_timer()
        self.lap_dict[self.counter] = (self.seconds, self.minutes, self.hours)
        self.counter += 1
        self.reset_lap_display()

    def reset_lap_display(self):
        self.display_laps.delete(0, tk.END)
        for num, (sec, min, hour) in self.lap_dict.items():
            self.display_laps.insert(tk.END, f"{num+1}. {hour:02}:{min:02}:{sec:02}")
        self.display_laps.pack()
