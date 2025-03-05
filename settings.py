import menu
import tkinter as tk
from tkinter import Toplevel
'''
This is the settings class that is used in all of the modules for the color customization

'''
class Settings(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.alert_label = tk.Label(self, text="The color settings will have to be modified using the text file", font=("Arial", 15), fg="red")
        self.alert_label.pack()

        self.leave = tk.Button(self, text="Back", command=lambda: controller.show_frame(menu.Start))    #Back button
        self.leave.pack()


    def selected_colors(self):

        self.options = {        #Default options/fallback options
            "button_menu": "gray",
            "button_back": "red",
            "background": "black",
            "listbox": "gray",
            "text": "black",
            "button_start": "green",
            "button_stop": "red",
            "button_lap": "orange",
            "increment": "dark green",
            "decrement": "dark red",
            "button_load": "gray",
            "button_save": "gray",
            "button_delete": "red"
        }

        black_list = "#"
        try:        #This is validation for if the file could not be found
            with open("settings.txt", "r") as file:
                for line in file:
                    line = line.strip()  
                    if black_list not in line and line: 
                        setting, option = line.split(":")  
                        self.options[setting.strip()] = (option.strip())
                        print(line)        #Debugging
        except FileNotFoundError:
            print("settings.txt could not be found using defaults and making file")
            with open("settings.txt", "a") as file:
                for key, value in self.options.items():
                    file.write(f"{key}:{value}\n")
        except:     #Will output a message if some other kind of error happens
            print("An error has happened using defaults")

        try:        
            for key, color in self.options.items():     #Will go through every item in the dictionary and make a variable for them, used for convenience 
                setattr(self, f"{key}_color", color)     
        except:
            print("Error")
        
        if (self.background_color == "black"):      #Sets the text color to the opposite of the background color
            self.title_text_color = "white"
        elif (self.background_color == "white"):
            self.title_text_color = "black"
        else:
            self.title_text_color = "white"         #Default text color
