import menu
import getpass
import tkinter as tk
from tkinter import Toplevel
class Other(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.username = getpass.getuser()

        
        self.other_label = tk.Label(self, text="Others menu", font=("Arial", 20))
        self.other_label.pack()
        self.progress_button = tk.Button(self, text="Progress", command=self.progress)
        self.progress_button.pack()

        self.leave = tk.Button(self, text="Back", command=lambda: controller.show_frame(menu.Start))
        self.leave.pack(padx=5)

    
    def progress(self):
        load_window = Toplevel(self)
        text_area = tk.Text(load_window, wrap=tk.WORD)
        text_area.pack()
        load_window.title("Progress")
        filepath = rf"C:\Users\{self.username}\Documents\Python\Final Project\stuff.txt"
        try:
            with open(filepath, 'r') as file:
                content = file.read()
                text_area.delete("1.0", tk.END)
                text_area.insert(tk.END, content)
        except Exception as e:
            print(f"Error {e}")
        text_area.config(state=tk.DISABLED)