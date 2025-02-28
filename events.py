import tkinter as tk
import menu
import datetime
import calendar
from tkinter import Toplevel

class Events(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.current_date = datetime.datetime.now().strftime("%d/%m/%Y")
        self.user_date = self.current_date.strip().split("/", 2)
        self.button_spaces = 2
        self.current_button = 0

        self.label = tk.Label(self, text=f"Events", font=("Arial", 10))
        self.label.pack()

        self.add_event = tk.Button(self, text="Add Event", command=self.add_event_dialog)
        self.add_event.pack(padx=5)

        self.current_events = tk.Listbox(self)
        self.load_saved_events()

        self.load_event = tk.Button(self, text="Change Settings", command=self.load_saved_events_output)
        self.load_event.pack()

        self.leave = tk.Button(self, text="Back", command=lambda: controller.show_frame(menu.Start))
        self.leave.pack(padx=5)

    def load_saved_events(self):
        self.events_list = {}
        self.current_events.delete(0, tk.END)
        try:
            with open("event_save.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                
                    event_name, event_day, event_month, event_year = line.strip().split(":", 3)
                    self.events_list[event_name] = (event_day, event_month, event_year)
                for name, (day, month, year) in self.events_list.items():
                    self.current_events.insert(tk.END, f"{name}: {int(day):02d}\{int(month):02d}\{int(year):02d}")
            self.current_events.pack()
        
        except FileNotFoundError:
            pass

    def load_saved_events_output(self):
        load_window = Toplevel(self)

        load_window.title("Edit Event?")
        load_window.geometry("300x300")

        self.load_window_lavel_select = tk.Label(load_window, text="Current Event Details")
        self.load_window_lavel_select.pack()
        self.current_name = self.current_events.get(tk.ACTIVE).split(":")[0]
        self.load_current_name = tk.Label(load_window, text=f"{self.current_name}")
        self.load_current_name.pack()

        for key, (day, month, year) in self.events_list.items():
            self.load_current_stats = tk.Label(load_window, text=f"{day}/{month}/{year}", font=("Arial", 10))

        self.load_current_stats.pack()

        self.edit_name = tk.Entry(load_window)
        self.edit_name.pack()

        self.change_name = tk.Button(load_window, text="confirm?", command=self.change_event_name)
        self.change_name.pack()
    
    def change_event_name(self):
        self.new_name = self.edit_name.get()
        self.events_list[self.new_name] = self.events_list[self.current_name]
        del self.events_list[self.current_name]
        with open("event_save.txt", "w") as file:
            for key, (day, month, year) in self.events_list.items():
                file.write(f"{key}:{day}:{month}:{year}\n")
        self.load_saved_events()

    def add_event_dialog(self):
        save_window = Toplevel(self)

        save_window.title("Create Event?")
        save_window.geometry("300x300")

        self.day = int(self.user_date[0])
        self.month = int(self.user_date[1])
        self.year = int(self.user_date[2])

        save_window_label_name = tk.Label(save_window, text="Enter the event name")
        save_window_label_name.pack()

        self.save_event_entry = tk.Entry(save_window)
        self.save_event_entry.pack()

        save_window_label_date = tk.Label(save_window, text="Enter the date")
        save_window_label_date.pack()

        #self.date_day_button_up = tk.Button(save_window, text="/\\", command=lambda: self.increment_date(0))
        #self.date_day_button_up.pack()
        button_frame_increment = tk.Frame(save_window)
        button_frame_increment.pack(pady=10)
        for i in range(3):
            self.button_increment = tk.Button(button_frame_increment, text=f"/\\", command=lambda i=i+1: self.buttons_up(i))
            self.button_increment.pack(side="left", padx=5)

        self.date_label = tk.Label(save_window, text=f"{self.user_date[0]}/{self.user_date[1]}/{self.user_date[2]}", font=("Arial", 20))
        self.date_label.pack()

        button_frame_decrement = tk.Frame(save_window)
        button_frame_decrement.pack(pady=10)
        for i in range(3):
            self.button_decrement = tk.Button(button_frame_decrement, text=f"\/", command=lambda i=i+1: self.buttons_low(i))
            self.button_decrement.pack(side="left", padx=5)

        self.create_event = tk.Button(save_window, text="Save", command=self.create_event)
        self.create_event.pack()
    def get_limit(self):
            self.max_days = calendar.monthrange(self.year, self.month)[1]
    def buttons_up(self, button_id): 
        if button_id == 1:
            self.increment_date(0)
        elif button_id == 2:
            self.increment_date(1)
        elif button_id == 3:
            self.increment_date(2)
    def buttons_low(self, button_id): 
        if button_id == 1:
            self.decrement_date(0)
        elif button_id == 2:
            self.decrement_date(1)
        elif button_id == 3:
            self.decrement_date(2)

    def increment_date(self, value):
        self.get_limit()
        self.user_date = [int(i) for i in self.user_date]
        if self.day < self.max_days and self.month in range(1, 12):  
            self.user_date[value] += 1
        elif self.day >= self.max_days:
            self.user_date[0] = 1 
            self.user_date[1] += 1
            if self.user_date[1] > 12: 
                self.user_date[1] = 1
                self.user_date[2] += 1
        elif self.month not in range(1, 12):  
            self.user_date[1] = 1 
        self.update_date()
        
    def decrement_date(self, value):
        self.get_limit()
        self.user_date = [int(i) for i in self.user_date]
        if self.user_date[value] > 1:  
            self.user_date[value] -= 1
        elif self.day <= 1:
            self.user_date[0] = self.max_days
            self.user_date[1] -= 1
            if self.user_date[1] < 1: 
                self.user_date[1] = 12
                self.user_date[2] -= 1
        elif self.month <= 1:  
            self.user_date[1] = 12 
            self.user_date[2] -= 1
        self.update_date()
    def update_date(self):
        self.day = int(self.user_date[0])
        self.month = int(self.user_date[1])
        self.year = int(self.user_date[2])
        self.date_label.config(text=f"{int(self.day):02d}/{int(self.month):02d}/{int(self.year)}", font=("Arial", 20))

    def create_event(self):
        self.title = self.save_event_entry.get()
        if not self.title:
            self.title = "unnamed event"
        with open("event_save.txt", "a") as file:
            file.write(f"{self.title}:{self.user_date[0]}:{self.user_date[1]}:{self.user_date[2]}\n")
        
        self.load_saved_events()