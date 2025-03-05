import tkinter as tk
import menu
import datetime
import calendar
import settings
from tkinter import Toplevel

class Events(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        settings.Settings.selected_colors(self)     #Gets custom colors
        self.configure(bg=self.background_color)    #Sets background
        self.current_date = datetime.datetime.now().strftime("%d/%m/%Y")    #Gets today's date

        self.current_date_list = self.current_date.strip().split("/", 2)    #Current date in a list

        self.user_date = self.current_date.strip().split("/", 2)    #User's custom date

        '''
        Just date seperated into three variables
        
        '''

        self.day = int(self.user_date[0])   
        self.month = int(self.user_date[1])
        self.year = int(self.user_date[2])

        self.label = tk.Label(self, text=f"Events", font=("Arial", 20), fg=self.title_text_color, bg=self.background_color) #Events button
        self.label.pack()

        self.current_events = tk.Listbox(self, bg=self.listbox_color)   #All events that are saved
        self.load_saved_events()

        self.add_event = tk.Button(self, text="Add Event", command=lambda: Create_events(self), bg=self.button_save_color)  #Add event
        self.add_event.pack(padx=5)

        self.load_event = tk.Button(self, text="Change Settings", command=lambda: Edit_events(self), bg=self.button_load_color) #Edit event configuration
        self.load_event.pack()

        self.leave = tk.Button(self, text="Back", command=lambda: controller.show_frame(menu.Start), bg=self.button_back_color) #Back button
        self.leave.pack(padx=5)
    '''
    Debugging for future stuff
    
    '''
    def check_active(self):
        
        self.today = datetime.datetime.now()

        if self.desired_date >= self.today:
            print("Active")
        else:
            print("In-active")

    def load_saved_events(self):
        self.events_list = {}   # Same thing as the load function in timer
        self.current_events.delete(0, tk.END)
        try:
            with open("event_save.txt", "r") as file:   #Opens event_save
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if line:    #Checks if line is blank or not
                        self.event_name, self.event_day, self.event_month, self.event_year = line.strip().split(":", 3) #Puts everythin in a list
                        self.desired_date = datetime.datetime(int(self.event_year), int(self.event_month), int(self.event_day)) #Selected date on the file
                        self.check_active() #Ignore, used for debugging future stuff
                        self.events_list[self.event_name] = (self.event_day, self.event_month, self.event_year) #Puts the event name into a dictionary
                for name, (day, month, year) in self.events_list.items():   #Inserts dictionary into the boxlist
                    self.current_events.insert(tk.END, f"{name}: {int(day)}/{int(month)}/{int(year)}")
            self.current_events.pack()  #Creates boxlist
            
        except FileNotFoundError:
            pass    #Skips
        except ValueError:
            print("This is has causes and error")



class Edit_events(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        settings.Settings.selected_colors(self) #Gets settings

        self.load_window = Toplevel(self, bg=self.background_color) #Creates window

        self.load_window.title("Edit Event?")   #Window name
        self.load_window.geometry("300x300")    #Window resolution

        self.parent_frame = self.master 

        self.load_window_lavel_select = tk.Label(self.load_window, text="Current Event Details", bg=self.background_color, fg=self.title_text_color)    #Current event details
        self.load_window_lavel_select.pack()
        self.event_list = self.parent_frame.events_list
        self.current_line = self.parent_frame.current_events.get(tk.ACTIVE).split(":")[0]   #Gets name of selected item in list
        self.load_current_stats = {}    #Selected dictionary
        try:
            with open("event_save.txt", 'r') as file:
                for line in file:
                    line = line.strip() 
                    print(line) #Debugging
                    if line: #Checks if line is not blank (input validation)
                        key, day, month, year = line.split(":") #Splits the line into a list 
                        if key.strip() == self.current_line:
                            self.load_current_stats[key.strip()] = (day.strip(), month.strip(), year.strip())   #Creates a dictionary with the name as key and everything after as its value, a key, tulple pair
        except FileNotFoundError:   
            print(f"Error: File event_save.txt not found.") #Debugging output
            return None
        except ValueError:
             print(f"Error: Invalid format")    #Debugging output
             return None
        
        for key, (day, month, year) in self.load_current_stats.items(): #Outputs the dictionary that was saved
            self.current_stats_label = tk.Label(self.load_window, text=f"{key}: {day}/{month}/{year}", bg=self.background_color, fg=self.title_text_color)
        self.current_stats_label.pack()

        self.edit_date = tk.Entry(self.load_window) #Edit date
        self.edit_date.pack()

        self.change_date = tk.Button(self.load_window, text="confirm?", command=self.change_event_date, bg=self.button_load_color)  #Confirm selection
        self.change_date.pack()

        self.delete_selection = tk.Button(self.load_window, text="delete", command=self.delete_event, bg=self.button_delete_color)  #Delete buttons
        self.delete_selection.pack()



    def change_event_date(self):
        self.new_date_user = self.edit_date.get()
        print(self.new_date_user)

        if not self.is_valid_date_format(self.new_date_user):   #Checks if the date the user input is valid
            print("Please use DD/MM/YYYY")
            return
    
        self.day, self.month, self.year = [int(x) for x in self.new_date_user.split("/")]   #Creates three values from the date the user input
        self.load_current_stats[self.current_line] = (self.day, self.month, self.year)
        self.write_to_file()    #Saves the date

    def delete_event(self):
        event_to_delete = self.current_line   #Get active selection
        print(event_to_delete)  #Debugging
        with open("event_save.txt", "r") as file:
            lines = file.readlines()
        
        with open("event_save.txt", "w") as file:
            for line in lines:
                event_name, _, _, _ = line.strip().split(":")
                if event_name != event_to_delete:
                    file.write(line)
    
        self.parent_frame.load_saved_events()    #Updates saved events
        self.load_window.destroy()  #Closes window
    
    def is_valid_date_format(self, date_str):
        parts = date_str.split("/")
        if len(parts) != 3: #Checks if the length is valid
            return False
        day, month, year = parts
        return day.isdigit() and month.isdigit() and year.isdigit() and len(day) == 2 and len(month) == 2 and len(year) == 4    #Massive truth statement if conditions are met the return True
    
    def write_to_file(self):    #Saves updated date
        with open("event_save.txt", "r") as file:
            lines = file.readlines()
        with open("event_save.txt", "w") as file:
            for line in lines:
                line = line.strip().split(":")  
                if line[0] == self.current_line:
                    file.write(f"{self.current_line}:{self.day}:{self.month}:{self.year}\n")
                else:
            
                    file.write(f"{line[0]}:{line[1]}:{line[2]}:{line[3]}\n")
        
        self.parent_frame.load_saved_events()
        self.load_window.destroy()  #Closes window


class Create_events(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        settings.Settings.selected_colors(self) #Custom color Settings

        self.save_window = self.load_window = Toplevel(self, bg=self.background_color)  #Background
        self.save_window.title("Create Event?") #Window title
        self.save_window.geometry("300x300")    #Resolution

        self.parent_frame = self.master #Gets values from previous class

        self.current_date = self.parent_frame.current_date  #Shortening variable
        self.user_date = self.parent_frame.user_date    #Shortening variable
        '''
        Shortening variables
        
        '''
        self.day = self.parent_frame.day
        self.month = self.parent_frame.month
        self.year = self.parent_frame.year

        save_window_label_name = tk.Label(self.save_window, text="Enter the event name", bg=self.background_color, fg=self.title_text_color)    #Enter name label
        save_window_label_name.pack()

        self.save_event_entry = tk.Entry(self.save_window)
        self.save_event_entry.pack()

        save_window_label_date = tk.Label(self.save_window, text="Enter the date", bg=self.background_color, fg=self.title_text_color)  #Enter date
        save_window_label_date.pack()

        button_frame_increment = tk.Frame(self.save_window, bg=self.background_color)   
        button_frame_increment.pack(pady=10)
        for i in range(3):  #Creates three buttons so the user can choose the date
            self.button_increment = tk.Button(button_frame_increment, text=f"/\\", command=lambda i=i+1: self.buttons_up(i), bg=self.increment_color)
            self.button_increment.pack(side="left", padx=5)

        self.date_label = tk.Label(self.save_window, text=f"{self.user_date[0]}/{self.user_date[1]}/{self.user_date[2]}", font=("Arial", 20), bg=self.background_color, fg=self.title_text_color)   #Date using DD/MM/YYYY
        self.date_label.pack()

        button_frame_decrement = tk.Frame(self.save_window, bg=self.background_color)   
        button_frame_decrement.pack(pady=10)
        for i in range(3):  #Creates three buttons
            self.button_decrement = tk.Button(button_frame_decrement, text=f"\/", command=lambda i=i+1: self.buttons_low(i), bg=self.decrement_color)
            self.button_decrement.pack(side="left", padx=5)

        self.create_event = tk.Button(self.save_window, text="Save", command=self.create_event, bg=self.button_save_color)
        self.create_event.pack()

    def get_limit(self):
            self.max_days = calendar.monthrange(self.year, self.month)[1]   #Gets the limit for each month
    def buttons_up(self, button_id): 
        if button_id == 1:
            self.increment_date(0)  #Use value increment date 0 if button ID is 1
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
        self.get_limit()    #Gets date limit
        self.user_date = [int(i) for i in self.user_date]   #Turns user date into a list

        if self.day < self.max_days and self.month in range(1, 12): #Checks if the user has reached the max value for day month or year
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
        
    def decrement_date(self, value):    #Does the same thing as increment date but in reverse
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

    def update_date(self):  #Updates the output
        self.day = int(self.user_date[0])
        self.month = int(self.user_date[1])
        self.year = int(self.user_date[2])
        self.date_label.config(text=f"{int(self.day):02d}/{int(self.month):02d}/{int(self.year)}", font=("Arial", 20))

    def create_event(self): #Creates the event and saves it to the text file
        self.title = self.save_event_entry.get()
        if not self.title:
            self.title = "unnamed event"
        with open("event_save.txt", "a") as file:
            file.write(f"{self.title}:{self.user_date[0]}:{self.user_date[1]}:{self.user_date[2]}\n")
         
        self.parent_frame.load_saved_events()

