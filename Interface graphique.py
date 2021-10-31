from PIL import Image, ImageTk
import tkinter as Tk
import os
import functools

os.chdir("D:\Cours 2A\Z-Repertoire Python")

root = Tk.Tk()
root.title("Configuration des zones de préhension")

ampoule_jpg = Image.open("ampoule.jpg")
ampoule = ImageTk.PhotoImage(ampoule_jpg)

c_image = Tk.Canvas(root, width = ampoule_jpg.size[0], height = ampoule_jpg.size[1])
c_image.create_image(0,0, anchor = Tk.NW, image=ampoule)
c_image.pack()

couleur = 'green'
coordsRect = [0,0,0,0]

def startTrace(event, couleur): # se déclenche au clic gauche pour commencer à tracer un rectangle
    global coordsRect
    coordsRect[0:2] = [event.x, event.y]
    rect = c_image.create_rectangle(coordsRect[0],coordsRect[1],coordsRect[0],coordsRect[1],outline = couleur, width = 3, fill = 'green', stipple='gray50')
    c_image.bind("<B1-Motion>", functools.partial(ajusterTaille, rectangle = rect, couleur = couleur))

def ajusterTaille(event, rectangle, couleur): # se déclenche en maintenant clic gauche et en bougeant la souris
                                                       # pour tracer le rectangle
    c_image.coords(rectangle,coordsRect[0],coordsRect[1],event.x,event.y)
    c_image.bind('<ButtonRelease-1>', functools.partial(finirTrace, rectangle = rectangle, couleur = couleur))

def finirTrace(event, rectangle, couleur): # se déclenche en relachant le clic gauche et termine le rectangle
    coordsRect[2:4] = [event.x,event.y]
    c_image.coords(coordsRect[0],coordsRect[1],coordsRect[2],coordsRect[3])
    delete_rect(rectangle)
    
def delete_rect(rectangle):
    c_image.delete(rectangle)

c_image.bind("<Button-1>", functools.partial(startTrace, couleur = couleur))

root.mainloop()
