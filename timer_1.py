import tkinter as tk
from tkinter import Toplevel
import menu
import time

class Timer(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.clock = 0
        self.active = False

        self.button_spaces = 2

        self.label = tk.Label(self, text=f"00:00", font=("Arial", 20))
        self.label.pack()

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        self.up_toggle = tk.Button(button_frame, text="/\\", command=self.increment_time)
        self.up_toggle.pack(side="left", padx=10) 

        self.down_toggle = tk.Button(button_frame, text="\\/", command=self.decrement_time)
        self.down_toggle.pack(side="left", padx=10)

        self.start_timer = tk.Button(self, text="Start", command=self.toggle)
        self.start_timer.pack(pady=5)

        button_frame_saves = tk.Frame(self)
        button_frame_saves.pack(pady=10)

        self.load_timer_toggle = tk.Button(button_frame_saves, text="Load", command=self.open_load_dialog)
        self.load_timer_toggle.pack(side="left", padx=10)

        self.save_timer_toggle = tk.Button(button_frame_saves, text="Save", command=self.open_dialog_timer_save)
        self.save_timer_toggle.pack(side="left", padx=10)

        self.leave = tk.Button(self, text="Back", command=lambda: controller.show_frame(menu.Start))
        self.leave.pack()

    def open_load_dialog(self):
        self.load_window = Toplevel(self)

        self.load_window.title("Load Timer?")
        self.load_window.geometry("300x300")
        self.timers_list = tk.Listbox(self.load_window)
        self.timers_list.pack(pady=10)
        self.load_saved_timers()

        if not self.timers:
            no_timers_label = tk.Label(self.load_window, text="No timers saved yet.")
            no_timers_label.pack(pady=10)
        
        self.error_label = tk.Label(self.load_window, text=" ", fg="red")
        self.error_label.pack()
            
        load_button = tk.Button(self.load_window, text="Load Selected Timer", 
                                command=self.load_selected_timer)
        load_button.pack(pady=10)
        self.erase_button = tk.Button(self.load_window, text="Delete Selected Timer",
                                command=self.erase_selected_timer)
        self.erase_button.pack()

    def load_timer_file(self):
        self.timers = {}
        try:
            with open("timer_save.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    print(line)
                    timer_name, timer_value = line.strip().split(":", 1)
                    self.timers[timer_name] = timer_value
        except FileNotFoundError:
            pass
                
         
    def load_saved_timers(self):
    
        self.timers_list.delete(0, tk.END)
    
        with open("timer_save.txt", "r") as file:
            self.load_timer_file()
            for timer in self.timers.keys():
                self.timers_list.insert(tk.END, timer) 

    
    def erase_selected_timer(self):
        timer_to_delete = self.timers_list.get(tk.ACTIVE)
        print(timer_to_delete)
        with open("timer_save.txt", "r") as file:
            lines = file.readlines()
        
        with open("timer_save.txt", "w") as file:
            for line in lines:
                timer_name, _ = line.strip().split(":")
                if timer_name != timer_to_delete:
                    file.write(line)
        self.load_saved_timers()

    def load_selected_timer(self):
        try:
            self.clock = int(self.timers[self.timers_list.get(tk.ACTIVE)])
            self.update_timer_display()
            print(self.clock)
            self.load_window.destroy()
        except ValueError as e:
            self.error_label.config(text="A value in timer_save.txt is using the incorrect format!")
            self.error_label.pack()
            print(f"{e}")

    def open_dialog_timer_save(self):
        self.save_window = Toplevel(self)

        self.save_window.title("Save Timer?")
        self.save_window.geometry("300x300")

        save_window_label_name = tk.Label(self.save_window, text="Enter the timer name")
        save_window_label_name.pack()

        self.save_timer_entry = tk.Entry(self.save_window)
        self.save_timer_entry.pack()

        self.error_label = tk.Label(self.save_window, text=" ", fg="red")
        self.error_label.pack()

        save_window_button = tk.Button(self.save_window, text="Save", command=self.save_timer)
        save_window_button.pack()
    
    def save_timer(self):
        self.load_timer_file()
        self.title = self.save_timer_entry.get()
        if not self.title:
            self.title = "unnamed"
        if ":" not in self.title and self.title not in self.timers.keys():
            with open("timer_save.txt", "a") as file:
                file.write(f"{self.title}:{self.clock}\n")
                self.save_window.destroy()
        elif ":" in self.title:
            self.error_label.config(text="Did not save, entry must not contain ':'")
            self.error_label.pack()
        elif self.title in self.timers.keys():                
            self.error_label.config(text="Did not save, entry must not be in the file")
            self.error_label.pack()     

        
    def update_timer_display(self):
        minutes, seconds = divmod(int(self.clock), 60)
        self.label.config(text=f"{minutes:02}:{seconds:02}")
    
    def increment_time(self):
        self.clock += 1
        self.update_timer_display()
    
    def decrement_time(self):
        if (self.clock > 0):
            self.clock -= 1
            self.update_timer_display()

    def toggle(self):
        if self.active:
            self.active = False
            self.start_timer.config(text="Start")
        else:
            self.active = True
            self.start_timer.config(text="Stop")
            self.update_timer()

    def update_timer(self):
        if self.clock > 0 and self.active:
            self.clock -= 1
            self.update_timer_display()
            self.after(1000, self.update_timer)  
        else:
            self.active = False
            self.start_timer.config(text="Start")
