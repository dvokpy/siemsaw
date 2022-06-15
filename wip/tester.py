#!/usr/bin/python3

import tkinter as tk

windrow = tk.Tk()

width = windrow.winfo_screenwidth()

height = windrow.winfo_screenheight()

windrow.title('Siemsaw')
windrow.mainloop()

print(f'{1}x{2}', width, height)