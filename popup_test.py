#creating popup menu in tkinter 
import tkinter as tk
import os

x = 1400
lastClickX = 0
lastClickY = 0
impath = 'C://Users/pantalaimon/Desktop/PlantGame/pyplant/img/'

class App:
    #creates parent window 
    def __init__(self):

        self.root = tk.Tk()

        #call the plant gif as a list of images
        happy_1 = [tk.PhotoImage(file=impath+'happy_1.gif',format = 'gif -index %i' %(i)) for i in range(4)] #new and happy plant, 4 frames      

        #plant window configuration
        self.root.config(highlightbackground='white')
        self.label = tk.Label(self.root, bd=0, bg='white')
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.geometry('400x450+1150+450')
        self.root.bind('<Button-1>', self.save_last_click_pos)
        self.root.bind('<B1-Motion>', self.dragging)
        self.root.wm_attributes('-transparentcolor','white')
        self.root.after(0, self.update, 0, happy_1)
        self.label.pack()

    def save_last_click_pos(self, event):
        global lastClickX, lastClickY
        lastClickX = event.x
        lastClickY = event.y

    def dragging(self, event):
        x, y = event.x - lastClickX + self.root.winfo_x(), event.y - lastClickY + self.root.winfo_y()
        self.root.geometry("+%s+%s" % (x , y))

    #making the gif work
    def update(self, ind, happy_1):
        frame = happy_1[ind]
        ind += 1
        print("happy_1", ind)
        if ind > 3:
            ind = 0
        self.label.configure(image=frame)
        self.root.after(250, update, ind)

	#create menu 
    def PopUp(self): 
        self.popup_menu = tk.Menu(self.root, tearoff = 0)
        self.popup_menu.add_command(label = "save and quit", command = self.root.destroy) 

	#display menu on right click 
    def do_popup(self,event): 
        try: 
            self.popup_menu.tk_popup(event.x_root, event.y_root) 
        finally:
            self.popup_menu.grab_release() 
	
    def run(self):
        self.popup()
        self.root.bind("<Button-3>",self.do_popup)
        self.root.mainloop()

a = App() 
a.run() 
