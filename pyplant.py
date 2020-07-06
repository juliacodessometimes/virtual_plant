import tkinter as tk
from PIL import ImageTk,Image

lastClickX = 0
lastClickY = 0
impath = '../virtual_plant/img/'

root = tk.Tk()
label = tk.Label(root, bd=0, bg='white')

#call the plant gif as a list of images
#new and happy plant, 4 frames:
happy_1 = [tk.PhotoImage(file=impath+'happy_1.gif',format = 'gif -index %i' %(i)) for i in range(5)]

def save_last_click_pos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y

def dragging(event):
    x, y = event.x - lastClickX + root.winfo_x(), event.y - lastClickY + root.winfo_y()
    root.geometry("+%s+%s" % (x , y))

#making the gif run
def update(ind):
    frame = happy_1[ind]
    ind += 1
    if ind > 4:
        ind = 0
    label.configure(image=frame)
    root.after(250, update, ind)

def popup(event):
    #popup menu
    global menu_img, water_img, exit_img, exit_press_img

    #reading in menu and button images
    menu_img = ImageTk.PhotoImage(Image.open(impath+'menu.jpg'))
    water_img = ImageTk.PhotoImage(Image.open (impath+'water.jpg'))
    exit_img = ImageTk.PhotoImage(Image.open (impath+'exit.jpg'))
    exit_press_img = ImageTk.PhotoImage(Image.open (impath+'exit_pressed.jpg'))


    #setting up popup window
    top = tk.Toplevel(bd=0, highlightthickness=0)
    top.overrideredirect(True)
    top.resizable(False, False)
    top.attributes('-topmost', True)
    top.geometry(f'{menu_img.width()}x{menu_img.height()}+{root.winfo_x()-250}+{root.winfo_y()-200}')
    
    #making menu image appear
    canvas = tk.Canvas(top, width=menu_img.width(), height=menu_img.height(), bd=0, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0,0, anchor='nw', image=menu_img)
    
    #making the buttons
    frame = tk.Frame(canvas)
    canvas.create_window((menu_img.width()-exit_img.width()+8), exit_img.height()-12, window=frame)
    button = tk.Button(frame, image=exit_img, command=top.destroy, bd=0, highlightthickness=0, anchor="ne")
    button.pack()

    

#plant window configuration
root.config(highlightbackground='white')
root.overrideredirect(True)
root.resizable(False, False)
root.attributes('-topmost', True)
root.bind('<Button-1>', save_last_click_pos)
root.bind('<B1-Motion>', dragging)
root.wm_attributes('-transparentcolor','white')
root.after(0, update, 0)

label.bind("<Button-3>", popup)
label.pack()

root.mainloop()