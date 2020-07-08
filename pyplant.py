import tkinter as tk
from PIL import ImageTk,Image

#path to images/gifs
impath = '../virtual_plant/img/'

#other variables for plant and popup windows
lastClickX, lastClickY = 0, 0
lastClickX_top, lastClickY_top = 0, 0

#begin the main plant window (root)
root = tk.Tk()

#call the plant gifs as a list of images
idle_1 = [tk.PhotoImage(file=impath+'idle_1.gif',format = 'gif -index %i' %(i)) for i in range(3)] #new idle plant, 3 frames
happy_1 = [tk.PhotoImage(file=impath+'happy_1.gif',format = 'gif -index %i' %(i)) for i in range(5)] #new and happy plant, 5 frames

#reading in menu and button images
menu_img = ImageTk.PhotoImage(Image.open(impath+'menu.jpg'))
water_img = ImageTk.PhotoImage(Image.open (impath+'water.jpg'))
water_press_img = ImageTk.PhotoImage(Image.open (impath+'water_pressed.jpg'))
savequit_img = ImageTk.PhotoImage(Image.open (impath+'savequit.jpg'))
savequit_press_img = ImageTk.PhotoImage(Image.open (impath+'savequit_pressed.jpg'))
exit_img = ImageTk.PhotoImage(Image.open (impath+'exit.jpg'))
exit_press_img = ImageTk.PhotoImage(Image.open (impath+'exit_pressed.jpg'))

#making the gif run
label = tk.Label(root, bd=0, bg='white')

def update(ind):
    frame = happy_1[ind]
    ind += 1
    if ind > 4:
        ind = 0
    label.configure(image=frame)
    root.after(250, update, ind)

def callback_function():
    print('pushed')

def save_function():
    #save game function
    print('saved')

def popup_menu_function(event):
    #popup menu function
    global top, menu_img, water_img, water_press_img, savequit_img, savequit_press_img, exit_img, exit_press_img, lastClickX_top, lastClickY_top

    if top is not None:
        top.destroy()

    #setting up popup window
    top = tk.Toplevel(bd=0, highlightthickness=0)

    def save_last_click_pos_top(event):
        global lastClickX_top, lastClickY_top
        lastClickX_top = event.x
        lastClickY_top = event.y

    def dragging_top(event):
        top_x, top_y = event.x - lastClickX_top + top.winfo_x(), event.y - lastClickY_top + top.winfo_y()
        top.geometry("+%s+%s" % (top_x , top_y))

    top.overrideredirect(True)
    top.resizable(False, False)
    top.attributes('-topmost', True)
    top.bind('<Button-1>', save_last_click_pos_top)
    top.bind('<B1-Motion>', dragging_top)
    top.geometry(f'{menu_img.width()}x{menu_img.height()}+{root.winfo_x()-250}+{root.winfo_y()-200}')
    
    #making menu image appear
    canvas = tk.Canvas(top, width=menu_img.width(), height=menu_img.height(), bd=0, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0,0, anchor='nw', image=menu_img)
    
    #making the buttons
    exit_btn = tk.Label(canvas, image=exit_img, bd=0, highlightthickness=0)
    water_btn = tk.Label(canvas, image=water_img, bd=0, highlightthickness=0)
    savequit_btn = tk.Label(canvas, image=savequit_img, bd=0, highlightthickness=0)

    #placing the buttons
    exit_btn.place(x=368, y=8, anchor='nw')
    water_btn.place(x=(menu_img.width()/2)-(water_img.width()/2), y=water_img.height(), anchor='nw')
    savequit_btn.place(x=(menu_img.width()/2)-(water_img.width()/2), y=(water_img.height()*3.5), anchor='sw')
    
    #defining button image change functions
    def water_press(event):
        water_btn.config(image=water_press_img)

    def water_release(event):
        water_btn.config(image=water_img)
        callback_function()
    
    def savequit_press(event):
        savequit_btn.config(image=savequit_press_img)
    
    def savequit_release(event):
        savequit_btn.config(image=savequit_img)
        save_function()
        root.destroy()

    def exit_press(event):
        exit_btn.config(image=exit_press_img)

    def exit_release(event):
        exit_btn.config(image=exit_img)
        top.destroy()
    
    #binding buttons to mouse click/release
    water_btn.bind('<ButtonPress-1>', water_press)
    water_btn.bind('<ButtonRelease-1>', water_release)
    savequit_btn.bind('<ButtonPress-1>', savequit_press)
    savequit_btn.bind('<ButtonRelease-1>', savequit_release)
    exit_btn.bind('<ButtonPress-1>', exit_press)
    exit_btn.bind('<ButtonRelease-1>', exit_release)
    
def save_last_click_pos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y

def dragging(event):
    x, y = event.x - lastClickX + root.winfo_x(), event.y - lastClickY + root.winfo_y()
    root.geometry("+%s+%s" % (x , y))

#plant window configuration
root.config(highlightbackground='white')
root.overrideredirect(True)
root.resizable(False, False)
root.attributes('-topmost', True)
root.bind('<Button-1>', save_last_click_pos)
root.bind('<B1-Motion>', dragging)
root.wm_attributes('-transparentcolor','white')
root.after(0, update, 0)

label.bind("<Button-3>", popup_menu_function)
label.pack()

top = None

root.mainloop()