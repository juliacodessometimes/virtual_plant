import tkinter as tk
import os
import fnmatch
from PIL import ImageTk,Image
from plant import Plant

impath = "../virtual_plant/img/"
gifpath = "../virtual_plant/gifs/"

def gameloop():
    delta = 100
    update(delta) # Updates data models.
    draw() # Render animation based on state of plant. 

    root.after(100, gameloop)

def update(delta):
    plant.update(delta)

def draw():
    # Draw the plant.
    label.configure(image=get_current_frame(plant))

    print(plant.mood, plant.new_mood, plant.config["number_of_frames"][plant.new_mood][plant.growth_stage])

def get_current_frame(plant):
    image_list = mapping[plant.mood][plant.growth_stage]
    return image_list[plant.current_index]

def gif_info (string):
    # Gets the mood, growth stage, and number of frames for each gif file
    split = string.split("_")
    gif_mood = split[0]
    gif_stage = split[1]
    gif_frames_num = split[2]

    return gif_mood, int(gif_stage), int(gif_frames_num)

def frame_list (file_name):
    # Creates list of images from the selected gif file
    frame_number = gif_info(str(file_name))[2]
    gif = [tk.PhotoImage(file=gifpath+str(file_name), format = 'gif -index %i' %(i)) for i in range(frame_number)]
    return gif

def water_function():
    plant.add_water(40)

def save_function():
    # Save game function (placeholder)
    print('saved')

def popup_menu_function(event):
    # Initiates the popup menu
    global top, menu_img, water_img, water_press_img, savequit_img, savequit_press_img, exit_img, exit_press_img, lastClickX_top, lastClickY_top

    if top is not None:
        top.destroy()
    
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

    # Makes menu image and button images appear
    canvas = tk.Canvas(top, width=menu_img.width(), height=menu_img.height(), bd=0, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0,0, anchor='nw', image=menu_img)
    
    exit_btn = tk.Label(canvas, image=exit_img, bd=0, highlightthickness=0)
    water_btn = tk.Label(canvas, image=water_img, bd=0, highlightthickness=0)
    savequit_btn = tk.Label(canvas, image=savequit_img, bd=0, highlightthickness=0)
    
    # Placing the buttons
    exit_btn.place(x=368, y=8, anchor='nw')
    water_btn.place(x=(menu_img.width()/2)-(water_img.width()/2), y=water_img.height(), anchor='nw')
    savequit_btn.place(x=(menu_img.width()/2)-(water_img.width()/2), y=(water_img.height()*3.5), anchor='sw')

    # Defining button image change functions
    def water_press(event):
        water_btn.config(image=water_press_img)

    def water_release(event):
        water_btn.config(image=water_img)
        water_function()
    
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

    # Binding buttons to mouse click/release
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


root = tk.Tk()

# Other variables for plant and popup windows.
# Used for drag and drop functionality.
lastClickX, lastClickY = 0, 0
lastClickX_top, lastClickY_top = 0, 0

# Reading in menu and button images.
menu_img = ImageTk.PhotoImage(Image.open(impath+'menu.jpg'))
water_img = ImageTk.PhotoImage(Image.open (impath+'water.jpg'))
water_press_img = ImageTk.PhotoImage(Image.open (impath+'water_pressed.jpg'))
savequit_img = ImageTk.PhotoImage(Image.open (impath+'savequit.jpg'))
savequit_press_img = ImageTk.PhotoImage(Image.open (impath+'savequit_pressed.jpg'))
exit_img = ImageTk.PhotoImage(Image.open (impath+'exit.jpg'))
exit_press_img = ImageTk.PhotoImage(Image.open (impath+'exit_pressed.jpg'))

# Each index in mapping represents a plant mood
# Each list item contains animation frames corresponding to the plant's mood at various stages of growth
mapping = {
        "dead": [],
        "shrivel": [],
        "droop": [],
        "limp": [],
        "perk": [],
        "idle": [],
        "happy": [],
        "grow": []
}


for file_name in sorted(os.listdir(gifpath)):
    mood, stage, frames = gif_info(file_name)

    mapping[mood].append(frame_list(file_name))
    Plant.config["number_of_frames"][mood].append(int(frames))

# Label that holds the plant images
label = tk.Label(root, bd=0, bg='white')

plant = Plant()

# Plant window configuration
root.config(highlightbackground='white')
root.overrideredirect(True)
root.resizable(False, False)
root.attributes('-topmost', True)
root.bind('<Button-1>', save_last_click_pos)
root.bind('<B1-Motion>', dragging)
root.wm_attributes('-transparentcolor','white')
root.after(0, gameloop)

label.bind("<Button-3>", popup_menu_function)
label.pack()

top = None
root.mainloop()