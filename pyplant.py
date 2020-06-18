import pyautogui
import tkinter as tk
import time
import os

x = 1400
lastClickX = 0
lastClickY = 0


def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y


def Dragging(event):
    x, y = event.x - lastClickX + window.winfo_x(), event.y - lastClickY + window.winfo_y()
    window.geometry("+%s+%s" % (x , y))


impath = 'C://Users/pantalaimon/Desktop/PlantGame/pyplant/img/'

#starting the tkinter window
window = tk.Tk()

#call the plant gifs as a list of images
happy_1 = [tk.PhotoImage(file=impath+'happy_1.gif',format = 'gif -index %i' %(i)) for i in range(4)] #new and happy, 4 frames
grow_1 = [tk.PhotoImage(file=impath+'grow_1.gif',format = 'gif -index %i' %(i)) for i in range(10)] #first growth, 10 frames

#making the gif work 
def update(ind):
    frame = happy_1[ind]
    ind += 1
    print("happy_1 ", ind)
    if ind > 3:
        ind = 0
    label.configure(image=frame)
    window.after(250, update, ind)

#window configuration
window.config(highlightbackground='white')
label = tk.Label(window,bd=0,bg='white')
window.overrideredirect(True)
window.attributes('-topmost', True)
window.geometry("400x450+1150+450")
window.bind('<Button-1>', SaveLastClickPos)
window.bind('<B1-Motion>', Dragging)
window.wm_attributes('-transparentcolor','white')
window.after(0, update, 0)
label.pack()

#loop the program so it runs

window.mainloop()