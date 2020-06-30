import tkinter as tk

lastClickX = 0
lastClickY = 0
impath = 'C://Users/pantalaimon/Desktop/PlantGame/pyplant/img/'

class App:
    #creates parent window 
    def __init__(self, window, label):

        self.root = window

        #call the plant gif as a list of images
        self.happy_1 = [tk.PhotoImage(file=impath+'happy_1.gif',format = 'gif -index %i' %(i)) for i in range(4)] #new and happy plant, 4 frames      

        #plant window configuration
        self.root.config(highlightbackground='white')
        self.label = label
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.bind('<Button-1>', self.save_last_click_pos)
        self.root.bind('<B1-Motion>', self.dragging)
        self.root.wm_attributes('-transparentcolor','white')
        self.root.after(0, self.update, 0)

        #popup menu
        self.popup_menu = tk.Menu(self.root, tearoff = 0)
        self.popup_menu.add_command(label = "save and quit", command = self.root.destroy)
        self.root.bind("<Button-3>",self.do_popup)
        self.label.pack()

    #allowing you to drag/drop transparent window
    def save_last_click_pos(self, event):
        global lastClickX, lastClickY
        lastClickX = event.x
        lastClickY = event.y

    def dragging(self, event):
        x, y = event.x - lastClickX + self.root.winfo_x(), event.y - lastClickY + self.root.winfo_y()
        self.root.geometry("+%s+%s" % (x , y))

    #making the gif run
    def update(self, ind):
        frame = self.happy_1[ind]
        ind += 1
        print("happy_1", ind)
        if ind > 3:
            ind = 0
        self.label.configure(image=frame)
        self.root.after(250, self.update, ind)

	#display menu on right click 
    def do_popup(self,event): 
        try: 
            self.popup_menu.tk_popup(event.x_root, event.y_root) 
        finally:
            self.popup_menu.grab_release() 

window = tk.Tk()
label = tk.Label(window, bd=0, bg='white')
a = App(window, label)
window.mainloop()