'''
Updates:
Added stopwatch
Added menu and frames

'''


import tkinter as tk
import menu
def main():
    version = "0.0.2"   
    root = menu.MainMenu()
    root.title(f"Timer {version}")
    root.geometry("300x300")
    root.mainloop()
    
if __name__ == '__main__':
    main()