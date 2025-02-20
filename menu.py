import tkinter as tk
import stopwatch
class MainMenu(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Start, stopwatch.Stopwatch, wip):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Start)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class Start(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.label_menu = tk.Label(self, text="Timer")
        self.label_menu.pack()
        self.stopwatch_select = tk.Button(self, text="Stopwatch", command=lambda: controller.show_frame(stopwatch.Stopwatch))
        self.stopwatch_select.pack()
        self.timer_select = tk.Button(self, text="Timer", command=lambda: controller.show_frame(wip))
        self.timer_select.pack()

class wip(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label_wip = tk.Label(self, text="This is not developed.")
        self.label_wip.pack()
        self.leave = tk.Button(self, text="Back", command=lambda: controller.show_frame(Start))
        self.leave.pack(side=tk.BOTTOM, fill=tk.X)


