from PIL import Image, ImageTk
import tkinter as tk
import pyautogui
import numpy                      #y, x
def mover_punto(x1, y1, x2, y2, pasos):
    puntos = []
    for i in range(pasos + 1):  
        t = i / pasos  
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        puntos.append((x, y))
    return puntos

def loading_loop(i=0):
    global tk_img
    global w
    global h
    velocidad = 10
    mouse_pos = pyautogui.position()
    dx = mouse_pos.x - w
    dy = mouse_pos.y - h

    distancia = round(max(1, (dx**2 + dy**2) ** 0.5))  # Evita división por 0

    nx = dx / distancia
    ny = dy / distancia

    w += round(nx * velocidad)
    h += round(ny * velocidad)
    print(f"Loop {i}")

    # Rotate the original image
    centered_obj = obj_size/ 2
    rotated_pil_img = pil_img.rotate(numpy.rad2deg(numpy.arctan2(-mouse_pos.y+(centered_obj+h), mouse_pos.x-(centered_obj+w))))
    tk_img = ImageTk.PhotoImage(rotated_pil_img)

    # print(numpy.rad2deg(numpy.arctan2(mouse_pos.y, mouse_pos.x)))


    canvas.delete("all")
    canvas.create_image(0, 0, image=tk_img, anchor="nw")
    
    root.geometry(f'125x125+{w}+{h}') 
    # Call `loading_loop(i+1)` after 200 milliseconds
    root.after(10, loading_loop, i+1)

# Load the original image

root = tk.Tk()
# Quitar bordes de la ventana
root.overrideredirect(True)
# Hacer el fondo transparente
root.attributes('-transparentcolor', 'gray')

# Crear un marco con color de fondo (igual que el transparente)
# frame = tk.Frame(root, bg="gray")
# frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(root, bg="gray", highlightthickness=0)
canvas.pack()

global w
global h
w = 200
h = 200
obj_size = 125
root.geometry(f'125x125+{w}+{h}') 
center_of_window = [0 + (w/2), 0+h/2]
print(center_of_window)
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

print(ws, hs)

pil_img = Image.open("image.png")

loading_loop()

# Bloquear combinaciones de teclas comunes para minimizar
root.bind("<Alt-F4>", lambda e: "break")    # Alt+F4
root.bind("<Control-w>", lambda e: "break") # Ctrl+W
root.bind("<Control-q>", lambda e: "break") # Ctrl+Q
root.bind("<Escape>", lambda e: "break")    # Esc

# Mantener la ventana al frente cada segundo
def mantener_al_frente():
    root.attributes('-topmost', True)
    root.after(1000, mantener_al_frente)

mantener_al_frente()

root.mainloop()