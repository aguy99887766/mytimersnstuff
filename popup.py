import menu
import tkinter as tk
class Popup(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        popup_window = tk.Toplevel(self)
        popup_window.title("About Project")
        popup_window.geometry("800x200")
        message = '''

Welcome to My Timer, this is a timer that you can customize and make your own. You the user are
allowed to fork this project, or modify the code in anyway. I allow the user to edit the text file 
to do what they want. The point of this project is to allow the user to change what they want.

                '''
        popup_window.lift() 
        popup_label = tk.Label(popup_window, text=message)
        popup_label.pack()

        self.leave = tk.Button(popup_window, text="Got it.", command=popup_window.destroy) 
        self.leave.pack(padx=5)
    
    
        