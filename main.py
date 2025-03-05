
import tkinter as tk
import menu

'''
Main window, title and version can be changed here
The very root of the project and what the computer will first go to
'''

def main():
    program = "My clock"    #Title name
    version = "03/05/25"    #Last updated
    root = menu.MainMenu()
    root.title(f"{program} version: {version}")     #Window title
    root.geometry("800x800")        #Resolution
    root.mainloop()
    
if __name__ == '__main__':
    main()
