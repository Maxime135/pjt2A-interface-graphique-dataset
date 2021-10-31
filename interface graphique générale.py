from tkinter import *
import os
import functools
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import numpy as np


class Textbox(Entry):
    def __init__(self,parent=None):
        self.__text = StringVar()
        super().__init__(parent, textvariable=self.__text)
        
    
    def get(self):
        return self.__text()
    
    def set(self,text): 
        return self.__text().set(text)





class Interface(Tk):
    def __init__(self):
        super().__init__()
        self.create_widgets()
        self.coordsRect = [0,0,0,0]

    def create_widgets(self):
        #création des cadres
        self.cadreFichier = Frame(self,width=700, height = 50, borderwidth=5,relief='groove')
        self.cadreFichier.pack(fill=BOTH)

        self.cadreZoneDessin = Frame(self,width=700, height = 600, borderwidth='5',relief='groove')
        self.cadreZoneDessin.pack(fill=BOTH)

        self.cadreSauvegarde = Frame(self,width=700, height = 50, borderwidth='5',relief='groove')
        self.cadreSauvegarde.pack(fill=BOTH)


    #-----------------cadre Importation fichiers--------------
        #path = ""
        #self.entry_fichier = Entry(self.cadreFichier,textvariable=path)
        #self.entry_fichier.pack(side=LEFT)
        
        self.label_title = Label(self.cadreFichier,text='Création du dataset pour la préhension d\'ampoules ',)
        self.label_title.pack(side=TOP)

        self.ouvrir_fichier =Button(self.cadreFichier, text="Charger image", command=self.load_file)
        self.ouvrir_fichier.pack(side=LEFT,padx=10,pady=10)
        

    #-----------------cadre zone de dessin--------------
        self.canvas = Canvas(self.cadreZoneDessin,width=400,height=400)
        self.canvas.pack(side=LEFT)
        
        
        self.liste_nom_zone_val = [-1,1]
        #self.liste_nom_zone = ["Zone interdite","Zone de préhension"]
        self.listeBox_zones = Listbox(self.cadreZoneDessin,selectmode=SINGLE,width=25,height=2)
        self.listeBox_zones.insert(1, "Zone interdite = -1")
        self.listeBox_zones.insert(1, "Zone de préhension = 1")
        self.listeBox_zones.pack(side=LEFT)
        #zone = self.listeBox_zones.curselection()

        self.button_draw_zone = Button(self.cadreZoneDessin, text="Tracer zone", command=self.draw_zone)
        self.button_draw_zone.pack(side=LEFT,padx=10,pady=10)

        self.button_effacer_zone = Button(self.cadreZoneDessin, text="Effacer dernière zone", command=self.delete_rect)
        self.button_effacer_zone.pack(side=LEFT,padx=10,pady=10)


    #-----------------cadre pour sauvegarder l'image de sortie--------------
        self.bouton_svg_img = Button(self.cadreSauvegarde, text="Sauvegarder l'image avec cadre", command=self.create_output_image)
        self.bouton_svg_img.pack(side=LEFT,padx=10,pady=10)

        self.bouton_next = Button(self.cadreSauvegarde,text='Image suivante', command=self.image_next)
        self.bouton_next.pack(side=LEFT,padx=10,pady=10)

        self.bouton_previous = Button(self.cadreSauvegarde,text='Image précédente', command=self.image_previous)
        self.bouton_previous.pack(side=LEFT,padx=10,pady=10)




    def load_multiple_files(self): #permet de charger plusieurs fichiers
        liste_image = askopenfilename(multiple=True)

        

    def load_file(self):
        finName=askopenfilename()
        if finName!="":
            #self.label1["text"]=finName
            #self.labelim['text']=finName.split('/')[-1]
            #création de l'image PIL
            self.image = Image.open(finName)
            #récupération de la taille de l'image
            self.width= self.image.width
            self.height=self.image.height
            #affichage de la taille de l'image
            #self.label2["text"]=str(width)+"X"+str(height)
            #adaptation de la taille du canvas à l'image
            self.canvas.config(width=self.width, height=self.height)
            #affichage de l'image
            self.photo=ImageTk.PhotoImage(self.image)
            self.canvas.create_image( 0,0, anchor = NW,image=self.photo)
    

    

    def startTrace(self,event, couleur): # se déclenche au clic gauche pour commencer à tracer un rectangle
        self.coordsRect[0:2] = [event.x, event.y]
        global rect
        rect = self.canvas.create_rectangle(self.coordsRect[0],self.coordsRect[1],self.coordsRect[0],self.coordsRect[1],outline = couleur, width = 3, fill = couleur, stipple='gray50')
        self.canvas.bind("<B1-Motion>", functools.partial(self.ajusterTaille, rectangle = rect, couleur = couleur))

    def ajusterTaille(self,event, rectangle, couleur): # se déclenche en maintenant clic gauche et en bougeant la souris
                                                        # pour tracer le rectangle
        self.canvas.coords(rectangle,self.coordsRect[0],self.coordsRect[1],event.x,event.y)
        self.canvas.bind('<ButtonRelease-1>', functools.partial(self.finirTrace, rectangle = rectangle, couleur = couleur))

    def finirTrace(self,event, rectangle, couleur): # se déclenche en relachant le clic gauche et termine le rectangle
        self.coordsRect[2:4] = [event.x,event.y]
        self.canvas.coords(self.coordsRect[0],self.coordsRect[1],self.coordsRect[2],self.coordsRect[3])
        #self.delete_rect(rectangle)
        
    def delete_rect(self):
        self.canvas.delete(rect)

    
    def draw_zone(self): #détermine la classe de la zone à tracer et la couleur du rectangle
        if self.listeBox_zones.curselection()[0]==0 :
            couleur = "red"
            zone_type = "forbidden"
            self.canvas.bind("<Button-1>", functools.partial(self.startTrace, couleur = couleur))
            rect_forbidden = self.coordsRect

        else:
            couleur = "green"
            zone_type = "authorized"
            self.canvas.bind("<Button-1>", functools.partial(self.startTrace, couleur = couleur))
            rect_authorized = self.coordsRect
        
    
#    def delete_zone(self): #supprime le dernier rectangle tracé
#        print("")
#        #à modifier
    
    def create_output_image(self): #créé et enregistre l'image de sortie avec les rectangle 1 et -1.
        self.output_img = np.zeros(self.image.shape())

        #à modifier
    
    def image_next(self): #affiche l'image suivante dans l'interface graphique
        print("")
        #à modifier
    
    def image_previous(self): #revient à l'image précédente dans l'interface graphique
        print("")
        #à modifier
        


#Démarrage
fenetre=Interface()
fenetre.mainloop()

