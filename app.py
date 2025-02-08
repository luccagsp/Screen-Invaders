from PIL import Image, ImageTk
import tkinter as tk
from pynput import mouse
import numpy
import ctypes
class Invader:
    def __init__(self, velocidad, x=0, y=0, imagename="sprite.png", rotate=True):
        self.alive = True
        self.rotate = rotate
        self.cursorTouched = False
        self.win = tk.Toplevel(root)
        self.img = Image.open("image.png")
        self.velocidad = velocidad
        self.win_w, self.win_h = x, y
        self.obj_size = 125
        self.canvas = tk.Canvas(self.win, bg="gray", highlightthickness=0)
        self.canvas.pack()
        win = self.win

        win.overrideredirect(True)
        win.attributes('-transparentcolor', 'gray')
        # Bloquear combinaciones de teclas comunes para minimizar
        win.bind("<Alt-F4>", lambda e: "break")    # Alt+F4
        win.bind("<Control-w>", lambda e: "break") # Ctrl+W
        win.bind("<Control-q>", lambda e: "break") # Ctrl+Q
        win.bind("<Escape>", lambda e: "break")    # Esc

    
        def mantener_al_frente():
            win.attributes('-topmost', True)
            win.after(1000, mantener_al_frente)
        mantener_al_frente()

        self.behaviour()
    def behaviour(self):
        if self.alive == False: 
            self.canvas.delete("all")
            self.win.destroy()
            return
        mouse_x, mouse_y = mouse.position[0], mouse.position[1]
        dx, dy = mouse_x-self.win_w, mouse_y-self.win_h
        distancia = round(max(1, (dx**2 + dy**2) ** 0.5))  # Evita división por 0
        if distancia < 63: 
            self.cursorTouched=True
            self.destroy()
            self.explosion(mouse_x, mouse_y)
        nx = dx / distancia
        ny = dy / distancia
        print(distancia)
        self.win_w += round(nx * self.velocidad)
        self.win_h += round(ny * self.velocidad)
        
        # Rotate the original image
        centered_obj = self.obj_size/ 2
        if self.rotate == True: render_img = self.img.rotate(numpy.rad2deg(numpy.arctan2(-mouse_y+(centered_obj+self.win_h), mouse_x-(centered_obj+self.win_w))))
        else:                   render_img = self.img
        self.tk_img = ImageTk.PhotoImage(render_img)
        
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.tk_img, anchor="nw")
        self.win.geometry(f'125x125+{self.win_w-62}+{self.win_h-62-title_bar_h}') 
        self.win.after(25, self.behaviour)
    def destroy(self):
        self.alive = False
    def explosion(self, mousex, mousey):
        win = tk.Toplevel(root)
        size = 300
        print(mousex, mousey)
        img = Image.open("./george.png")
        canvas = tk.Canvas(win, bg="gray", highlightthickness=0)
        canvas.pack()
        win.geometry(f'300x265+{mousex-125}+{mousey-125}') 

        win.overrideredirect(True)
        win.attributes('-transparentcolor', 'gray')
        self.explosion_behaviour(img, canvas, size)
    def explosion_behaviour(self, img, canvas, size):
        

        img = img.resize((size,size), Image.LANCZOS)
        self.final_img = ImageTk.PhotoImage(img)
        canvas.delete("all")
        canvas.create_image(300/2, 300/2, image=self.final_img, anchor=tk.CENTER)
        size = size-5
        if size < 50:
            canvas.delete("all")
            return
        self.win.after(10, self.explosion_behaviour, img, canvas, size)




root = tk.Tk()
mouse = mouse.Controller()
ctypes.windll.shcore.SetProcessDpiAwareness(2)
title_bar_h = ctypes.windll.user32.GetSystemMetrics(4)

# Bloquear combinaciones de teclas comunes para minimizar
root.bind("<Alt-F4>", lambda e: "break")    # Alt+F4
root.bind("<Control-w>", lambda e: "break") # Ctrl+W
root.bind("<Control-q>", lambda e: "break") # Ctrl+Q
root.bind("<Escape>", lambda e: "break")    # Esc
# Quitar bordes de la ventana
root.overrideredirect(True)
# Hacer fondo transparente
root.attributes('-transparentcolor', 'gray')
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

canvas = tk.Canvas(root, bg="gray", highlightthickness=0)
canvas.pack()

asd = Invader(velocidad=4, x=1000, y=200)
explode = True
def mantener_al_frente(explode):
    if (asd.cursorTouched == True ) and explode == True:
        asd.destroy()
        print("a")
        inv1 = Invader(velocidad=5, x=-125, y=-125, rotate=False)
        inv2 = Invader(velocidad=5, x=ws+125, y=-125)
        inv1 = Invader(velocidad=5, x=-125, y=hs-125)
        inv2 = Invader(velocidad=5, x=ws-125, y=hs-125)
        explode = False


    root.attributes('-topmost', True)
    root.after(50, mantener_al_frente, explode)

mantener_al_frente(explode)

root.mainloop()