import tkinter as tk
import time
import settings
import menu
'''
The stopwatch class lets the user press start and track time

'''
class Stopwatch(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        settings.Settings.selected_colors(self)

        self.configure(bg=self.background_color)

        self.start_time = 0     #Default value
        self.active = False     #Checks if the stopwatch is active
        self.elasp = 0          #How much time has elapsed overall
        self.lap_dict = {}      #Tracks the laps 
        self.counter = 0        #Current number of laps

        self.label = tk.Label(self, text="00:00:00", bg=self.background_color, fg=self.title_text_color, font=("Arial", 15))    #Default timer message
        self.label.pack(pady=20)

        self.toggle = tk.Button(self, text="Start", command=self.toggle, bg=self.button_start_color)    #Start button
        self.toggle.pack(pady=5)

        self.toggle_lap = tk.Button(self, text="Lap", command=self.lap, state=tk.DISABLED, bg=self.button_lap_color)    #Lap button
        self.toggle_lap.pack()

        self.display_laps = tk.Listbox(self, bg=self.listbox_color) #Displays all the laps in the dictionary
        self.reset_lap_display()

        self.leave = tk.Button(self, text="Back", command=lambda: controller.show_frame(menu.Start), bg=self.button_back_color) #Back button
        self.leave.pack()
    
    def toggle(self):
        if self.active: #Checks if active and if it is will disable and reset everything or will active the stopwatch
            self.active = False
            self.toggle_lap.config(state=tk.DISABLED)
            self.toggle.config(text="Start", bg=self.button_start_color)
            self.lap_dict.clear()
            self.counter = 0
            self.reset_lap_display()
        else:
            self.active = True
            self.start_time = time.time() - self.elasp
            self.toggle_lap.config(state=tk.NORMAL)
            self.toggle.config(text="Stop", bg=self.button_stop_color)
            self.update_timer()
            
    def convert_timer(self):    #Converts the integar value that is increasing into human readible time
        current_time = time.time() - self.start_time    
        self.elapsed_time = current_time
        self.hours, self.rem_seconds = divmod(int(self.elapsed_time), 3600)   
        self.minutes, self.seconds = divmod(int(self.rem_seconds), 60)

    def update_timer(self):
        if self.active:     #Checks if the timer is active and updates the label to the time
            self.convert_timer()
            self.label.config(text=f"{self.hours:02}:{self.minutes:02}:{self.seconds:02}")
            self.after(1000, self.update_timer)     #Waits 1 second to update again
        
    def lap(self):
        self.convert_timer()    #Allows the user to save how long something was
        self.lap_dict[self.counter] = (self.seconds, self.minutes, self.hours)
        self.counter += 1
        self.reset_lap_display()

    def reset_lap_display(self):
        self.display_laps.delete(0, tk.END)     #Adds a new value to the lap list or resets it completely
        for num, (sec, min, hour) in self.lap_dict.items():
            self.display_laps.insert(tk.END, f"{num+1}. {hour:02}:{min:02}:{sec:02}")
        self.display_laps.pack()
