    
import tkinter as tk
import time
import menu
class Stopwatch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.start_time = 0
        self.active = False
        self.elasp = 0

        self.label = tk.Label(self, text="00:00")
        self.label.pack(pady=20)

        self.toggle = tk.Button(self, text="Start", command=self.toggle)
        self.toggle.pack(pady=5)
        self.leave = tk.Button(self, text="Back", command=lambda: controller.show_frame(menu.Start))
        self.leave.pack()
    
    def toggle(self):
        if self.active:
            self.active = False
            self.toggle.config(text="Start")
        else:
            self.active = True
            self.start_time = time.time() - self.elasp
            self.toggle.config(text="Stop")
            self.update_timer()
            
    
    def update_timer(self):
        if self.active:
            current_time = time.time() - self.start_time
            self.elapsed_time = current_time
            minutes, seconds = divmod(int(current_time), 60)
            self.label.config(text=f"{minutes:02}:{seconds:02}")
            self.after(1000, self.update_timer) 
        
    