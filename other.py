import menu
import popup
import getpass
import tkinter as tk
from tkinter import Toplevel
import os
'''
This area is not really important to the project but is used to track my progress and what I wanted to add to the project

'''
class Other(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.username = getpass.getuser()   #Gets the user's name of their computer

        
        
        self.other_label = tk.Label(self, text="Other Stuff", font=("Arial", 20))   #Set top lable
        self.other_label.pack()
        self.progress_button = tk.Button(self, text="Progress", command=self.progress) #Progress button
        self.progress_button.pack()
        self.popup_button = tk.Button(self, text="About the project", command=self.load_popup)  #Opens popup
        self.popup_button.pack()
        
        self.leave = tk.Button(self, text="Back", command=lambda: controller.show_frame(menu.Start))
        self.leave.pack(padx=5)

    def load_popup(self):
        popup.Popup(tk.Frame(self), self)  
    

    def progress(self):
        load_window = Toplevel(self)
        text_area = tk.Text(load_window, wrap=tk.WORD)
        text_area.pack()
        load_window.title("Progress")
        filepath = rf"C:\Users\{self.username}\Documents\Python\Final Project\stuff.txt"      #Filepath of the document that is needed
        try:
            with open(filepath, 'r') as file:       #Opens a window for the user to read the contents of the text
                content = file.read()
                text_area.delete("1.0", tk.END)
                text_area.insert(tk.END, content)
        except Exception as e:
            print(f"Error {e}")
        text_area.config(state=tk.DISABLED)