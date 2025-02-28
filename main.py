
import tkinter as tk
import menu

'''
Main window, title and version can be changed here
'''

def main():
    program = "My clock"
    version = "02/27/25"   
    root = menu.MainMenu()
    root.title(f"{program} version: {version}")
    root.geometry("300x300")
    root.mainloop()
    
if __name__ == '__main__':
    main()