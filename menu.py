import tkinter as tk
import other
import stopwatch
import events
import timer_1

class MainMenu(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Start, stopwatch.Stopwatch, wip, timer_1.Timer, events.Events, other.Other):
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

        self.other_select = tk.Button(self, text="Other", command=lambda: controller.show_frame(other.Other))
        self.other_select.pack(side="top", anchor="w", pady=5, padx=10)

        self.label_menu = tk.Label(self, text="My Clock")
        self.label_menu.pack(pady=20)

        self.stopwatch_select = tk.Button(self, text="Stopwatch", command=lambda: controller.show_frame(stopwatch.Stopwatch))
        self.stopwatch_select.pack(pady=5)
        self.timer_select = tk.Button(self, text="Timer", command=lambda: controller.show_frame(timer_1.Timer))
        self.timer_select.pack(pady=5)
        self.scheduler_select = tk.Button(self, text="Events", command=lambda: controller.show_frame(events.Events))
        self.scheduler_select.pack(pady=5)
        self.settings_select = tk.Button(self, text="Settings", command=lambda: controller.show_frame(wip))
        self.settings_select.pack(pady=5)

class wip(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label_wip = tk.Label(self, text="This is not developed.")
        self.label_wip.pack()
        self.leave = tk.Button(self, text="Back", command=lambda: controller.show_frame(Start))
        self.leave.pack(side=tk.BOTTOM, fill=tk.X)




