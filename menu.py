import tkinter as tk
import other
import stopwatch
import events
import timer_1
import settings
'''
This is the main menu class and is used when the user decides to start the program


This entire area is where the user is most of the time, everything is controlled by frame which lets the user navigate without having to deal with
many different windows at once.
'''
class MainMenu(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)      

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Start, stopwatch.Stopwatch, timer_1.Timer, events.Events, other.Other, settings.Settings):    #Each menu the user can select
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    

        self.show_frame(Start)      

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class Start(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        settings.Settings.selected_colors(self)     #This is for the user's configuration    

        self.configure(bg=self.background_color)    #This sets the background to whatever the user choose 

        self.other_select = tk.Button(self, text="Other", command=lambda: controller.show_frame(other.Other), bg=self.button_menu_color)        #This is the others menu that is located on the top left of the screen
        self.other_select.pack(side="top", anchor="w", pady=5, padx=10)     

        self.label_menu = tk.Label(self, text="𝓜𝔂 𝓒𝓵𝓸𝓬𝓴", font=("Arial", 20), bg=self.background_color, fg=self.title_text_color)       #This is the name of the program
        self.label_menu.pack(pady=20)

        self.stopwatch_select = tk.Button(self, text="Stopwatch", command=lambda: controller.show_frame(stopwatch.Stopwatch), bg=self.button_menu_color)        #This is the stopwatch and will bring the user to the stopwatch
        self.stopwatch_select.pack(pady=5)
        self.timer_select = tk.Button(self, text="Timer", command=lambda: controller.show_frame(timer_1.Timer), bg=self.button_menu_color)      #Timer button
        self.timer_select.pack(pady=5)
        self.scheduler_select = tk.Button(self, text="Events", command=lambda: controller.show_frame(events.Events), bg=self.button_menu_color)     #Events button
        self.scheduler_select.pack(pady=5)
        self.settings_select = tk.Button(self, text="Settings", command=lambda: controller.show_frame(settings.Settings), bg=self.button_menu_color)    #Settings button
        self.settings_select.pack(pady=5)
        self.exit_program = tk.Button(self, text="Exit Program", command=self.leave, bg=self.button_back_color)
        self.exit_program.pack(pady=5)

    def leave(self):
        self.quit()