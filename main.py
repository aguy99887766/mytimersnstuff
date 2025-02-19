'''
Updates:
Added stopwatch

'''


import tkinter as tk
import GUI
def main():
    version = "0.0.1"   
    root = GUI.stopwatch()
    root.title(f"Timer {version}")
    root.geometry("300x300")
    root.mainloop()
    
if __name__ == '__main__':
    main()