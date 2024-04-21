import tkinter as tk
import random

root = tk.Tk()
root.title("Floppy Totoro")
canvas = tk.Canvas(root, width=800, height=800, bg="skyblue")
canvas.pack()

circle = canvas.create_oval(42, 70, 92, 100, fill="green")

def test():
    canvas.move(circle, 0, 1)
    coordOfCircle = canvas.coords(circle)
    if coordOfCircle[3] > 800:
        return
    root.after(10, test)
    

test()
root.mainloop()