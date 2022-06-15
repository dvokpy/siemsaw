#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk

#Grabs dimensions for window and returns a string "widthxheight"
def dimension_grabber(screen):
    width = screen.winfo_screenwidth()
    height = screen.winfo_screenheight()
    dimensions = "{0}x{1}+50+50".format(int(width/1.5), int(height/1.5))
    return dimensions

#Builds out main window
def main_window_gen():
    top_window = tk.Tk()
    top_window.title("Siemsaw")
    top_window.geometry(dimension_grabber(top_window))
    top_window.minsize(900, 450)
    top_window.mainloop()
    top_window.attributes('-topmost', 1)
    
def main():
    main_window_gen()
    

if __name__ == "__main__":
    main()