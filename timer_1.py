import tkinter as tk
from tkinter import Toplevel
import menu
import settings
import time
'''
Lets users start a timer aswell as save and load there own time they created
'''
class Timer(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        settings.Settings.selected_colors(self)     #Calls the function selected_colors from settings

        self.configure(bg=self.background_color)    #Sets the background color to the user's choosing 

        self.clock = 0          #Default value for the timer
        self.active = False     #Checks if active

        self.label = tk.Label(self, text=f"00:00", fg=self.title_text_color, bg=self.background_color, font=("Arial", 20))      #Default time
        self.label.pack()

        button_frame = tk.Frame(self, bg=self.background_color)     #Group for each of the buttons
        button_frame.pack(pady=10)

        self.up_toggle = tk.Button(button_frame, text="/\\", command=self.increment_time, bg=self.increment_color)      #Increments value by one
        self.up_toggle.pack(side="left", padx=10) 

        self.down_toggle = tk.Button(button_frame, text="\\/", command=self.decrement_time, bg=self.decrement_color)    #Decrements value by one
        self.down_toggle.pack(side="left", padx=10)
    
        self.start_timer = tk.Button(self, text="Start", command=self.toggle, bg=self.button_start_color)       #Starts timer
        self.start_timer.pack(pady=5)

        button_frame_saves = tk.Frame(self, bg=self.background_color)   #Groups save and load
        button_frame_saves.pack(pady=10)

        self.load_timer_toggle = tk.Button(button_frame_saves, text="Load", command=self.open_load_dialog, bg=self.button_load_color)   #Opens load window
        self.load_timer_toggle.pack(side="left", padx=10)

        self.save_timer_toggle = tk.Button(button_frame_saves, text="Save", command=self.open_dialog_timer_save, bg=self.button_save_color)     #Opens save window
        self.save_timer_toggle.pack(side="left", padx=10)

        self.leave = tk.Button(self, text="Back", command=lambda: controller.show_frame(menu.Start), bg=self.button_back_color)     #Back button
        self.leave.pack()

    def open_load_dialog(self):
        self.load_window = Toplevel(self, bg=self.background_color) #Creates new window

        self.load_window.title("Load Timer?")       #Sets window title
        self.load_window.geometry("300x400")        #Sets resolution
        '''
        Creates boxlist -> updates boxlist
        
        '''
        self.timers_list = tk.Listbox(self.load_window, bg=self.listbox_color)      #Shows the list of available timers
        self.timers_list.pack(pady=10)
        self.load_saved_timers()        #Loads the saved timers

        if not self.timers:     #If there are no saved timers then will put 'No timers saved.'"
            no_timers_label = tk.Label(self.load_window, text="No timers saved yet.", bg=self.background_color, fg=self.title_text_color)
            no_timers_label.pack(pady=10)
        
        self.error_label = tk.Label(self.load_window, text=" ", fg="red", bg=self.background_color) #Error message for user
        self.error_label.pack()
            
        load_button = tk.Button(self.load_window, text="Load Selected Timer",       
                                command=self.load_selected_timer, bg=self.button_load_color)        #Load Timer
        load_button.pack(pady=10)
        self.erase_button = tk.Button(self.load_window, text="Delete Selected Timer",
                                command=self.erase_selected_timer, bg=self.button_delete_color)     #Delete Timer
        self.erase_button.pack()

    def load_timer_file(self):
        self.timers = {}        #Timers spotted
        try:
            with open("timer_save.txt", "r") as file:   #Reads timers from the file and if they are found will add them
                lines = file.readlines()
                for line in lines:
                    line_check = line.split()
                    if line_check:
                        print(line)
                        timer_name, timer_value = line.strip().split(":", 1)
                        self.timers[timer_name] = timer_value
        except FileNotFoundError:
            pass

                
    '''
    Delete old boxlist -> loads dictionary -> goes through dictionary to insert each key, value pair to the boxlist
    '''
    def load_saved_timers(self):    #Adds timers to the boxlist
    
        self.timers_list.delete(0, tk.END)
        try:
            
            self.load_timer_file()
            for timer in self.timers.keys():
                self.timers_list.insert(tk.END, timer) 
        except:
            print("Something went wrong")

    '''
    Selected boxlist timer -> sets lines to the line size -> goes through eachline and if it is not the timer then rewrites the line
    '''
    def erase_selected_timer(self):     #Erases timers
        timer_to_delete = self.timers_list.get(tk.ACTIVE)   #Get active selection
        print(timer_to_delete)  #Debugging
        try:
            with open("timer_save.txt", "r") as file:
                lines = file.readlines()
            
            with open("timer_save.txt", "w") as file:
                for line in lines:
                    timer_name, _ = line.strip().split(":")
                    if timer_name != timer_to_delete:
                        file.write(line)
            self.load_saved_timers()    #Updates saved timers
        except ValueError as e:
            self.error_label.config(text="This value is using the incorrect format, but was deleted")    #Error message
            self.error_label.pack()
            print(f"{e}")
            self.load_saved_timers()    #Updates saved timers
        except FileNotFoundError:
            self.error_label.config(text="File could not be found")    #Error message
            self.error_label.pack()
            print(f"{e}")
        except:
            self.error_label.config(text="Something went wrong...")    #Error message
            self.error_label.pack()
            print(f"{e}")
        

    def load_selected_timer(self):  #Loads the selected timer
        try:    #Checks the format of the file to see if the user put something incorrectly without errors
            self.clock = int(self.timers[self.timers_list.get(tk.ACTIVE)])  #sets the clock to what the user is selecting
            self.update_timer_display() #Updates timer to match user's time
            print(self.clock)   #Debugging
            self.load_window.destroy()  #Closes window
        except ValueError as e:    
            self.error_label.config(text="A value in timer_save.txt is using the incorrect format!")    #Error message
            self.error_label.pack()
            print(f"{e}")

    def open_dialog_timer_save(self):       #Save timer
        self.save_window = Toplevel(self, bg=self.background_color)

        self.save_window.title("Save Timer?")       #Window title
        self.save_window.geometry("300x400")        #Resolution

        save_window_label_name = tk.Label(self.save_window, text="Enter the timer name", fg=self.title_text_color, bg=self.background_color)    #Name label
        save_window_label_name.pack()

        self.save_timer_entry = tk.Entry(self.save_window)  #Timer name
        self.save_timer_entry.pack()

        self.error_label = tk.Label(self.save_window, text=" ", fg="red", bg=self.background_color)     #Error message
        self.error_label.pack()

        save_window_button = tk.Button(self.save_window, text="Save", command=self.save_timer, bg=self.button_save_color)   # Save button
        save_window_button.pack()
    
    def save_timer(self):
        self.load_timer_file()  #Loads all current timers
        self.title = self.save_timer_entry.get()
        if not self.title:  #Unnamed timer
            self.title = "unnamed"
        if ":" not in self.title and self.title not in self.timers.keys():  #Saves timer
            with open("timer_save.txt", "a") as file:
                file.write(f"{self.title}:{self.clock}\n")
                self.save_window.destroy()
        elif ":" in self.title:     #Outputs error
            self.error_label.config(text="Did not save, entry must not contain ':'")
            self.error_label.pack()
        elif self.title in self.timers.keys():      #Outputs error    
            self.error_label.config(text="Did not save, entry must not be in the file")
            self.error_label.pack()     

        
    def update_timer_display(self):     #Updates what the clock
        minutes, seconds = divmod(int(self.clock), 60)
        self.label.config(text=f"{minutes:02}:{seconds:02}")
    
    def increment_time(self):
        self.clock += 1    #Increments the clock by one
        self.update_timer_display() #Updates user's clock
    
    def decrement_time(self):
        if (self.clock > 0):
            self.clock -= 1     #Decrements the clock by one
            self.update_timer_display() #Updates user's clock

    def toggle(self):
        if self.active: #Similar to the stopwatch toggle, if it's active set text to Start else Stop 
            self.active = False
            self.start_timer.config(text="Start", bg=self.button_start_color)
        else:
            self.active = True
            self.start_timer.config(text="Stop", bg=self.button_stop_color)
            self.update_timer()     #Updates the timer

    def update_timer(self): #Similar to stopwatch
        if self.clock > 0 and self.active:  
            self.clock -= 1 #Decrement clock by one
            self.update_timer_display() #Updates display
            self.after(1000, self.update_timer) #Waits 1 second
        else:   #Needed or else the whole thing breaks
            self.active = False
            self.start_timer.config(text="Start", bg=self.button_start_color)
