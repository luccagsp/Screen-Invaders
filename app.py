from PIL import Image, ImageTk
import tkinter as tk
from pynput import mouse
import numpy

class Invader:
    def __init__(self, velocidad, x=0, y=0):
        self.alive = True
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
            self.win.destroy
            return
        mouse_x, mouse_y = mouse.position[0], mouse.position[1]
        dx, dy = mouse_x-self.win_w, mouse_y-self.win_h
        distancia = round(max(1, (dx**2 + dy**2) ** 0.5))  # Evita división por 0
        if distancia < 10: self.cursorTouched=True
        nx = dx / distancia
        ny = dy / distancia

        self.win_w += round(nx * self.velocidad)
        self.win_h += round(ny * self.velocidad)
        
        # Rotate the original image
        centered_obj = self.obj_size/ 2
        rotated_img = self.img.rotate(numpy.rad2deg(numpy.arctan2(-mouse_y+(centered_obj+self.win_h), mouse_x-(centered_obj+self.win_w))))
        self.tk_img = ImageTk.PhotoImage(rotated_img)
        
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.tk_img, anchor="nw")
        self.win.geometry(f'125x125+{self.win_w}+{self.win_h}') 
        self.win.after(10, self.behaviour)
    def destroy(self):
        self.alive = False

root = tk.Tk()
mouse = mouse.Controller()

# Bloquear combinaciones de teclas comunes para minimizar
root.bind("<Alt-F4>", lambda e: "break")    # Alt+F4
root.bind("<Control-w>", lambda e: "break") # Ctrl+W
root.bind("<Control-q>", lambda e: "break") # Ctrl+Q
root.bind("<Escape>", lambda e: "break")    # Esc
# Quitar bordes de la ventana
root.overrideredirect(True)
# Hacer fondo transparente
root.attributes('-transparentcolor', 'gray')

canvas = tk.Canvas(root, bg="gray", highlightthickness=0)
canvas.pack()

asd = Invader(velocidad=4, x=1000, y=200)
asd2 = Invader(velocidad=10, x=0, y=200)
explode = True
def mantener_al_frente(explode):
    if (asd.cursorTouched == True or asd2.cursorTouched==True) and explode == True:
        asd.destroy()
        asd2.destroy()
        print("a")
        inv1 = Invader(velocidad=3, x=0, y=0)
        inv2 = Invader(velocidad=3, x=1200, y=0)
        inv1 = Invader(velocidad=3, x=0, y=1000)
        inv2 = Invader(velocidad=3, x=1000, y=1000)
        explode = False


    root.attributes('-topmost', True)
    root.after(50, mantener_al_frente, explode)

mantener_al_frente(explode)

root.mainloop()