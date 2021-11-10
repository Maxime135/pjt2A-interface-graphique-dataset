from tkinter import *
import os
import functools
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt

os.chdir=(os.getcwd()+"\\images ampoules\\")

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
        self.coordsRect_green = [0,0,0,0]
        self.coordsRect_red = [0,0,0,0]

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

        self.ouvrir_fichier =Button(self.cadreFichier, text="Charger images", command=self.load_multiple_files)
        self.ouvrir_fichier.pack(side=LEFT,padx=10,pady=10)
        

    #-----------------cadre zone de dessin--------------
        
        #self.texte_label_image_name = StringVar()
        self.label_image_name = Label(self.cadreZoneDessin)
        self.label_image_name.pack(side=TOP,padx=10,pady=10)
        
        self.canvas = Canvas(self.cadreZoneDessin,width=400,height=400)
        self.canvas.pack(side=LEFT)
        
        
        #self.liste_nom_zone_val = [-1,1]
        #self.liste_nom_zone = ["Zone interdite","Zone de préhension"]
        self.listeBox_zones = Listbox(self.cadreZoneDessin,selectmode=SINGLE,width=25,height=2)
        self.listeBox_zones.insert(1, "Zone interdite = -1")
        self.listeBox_zones.insert(1, "Zone de préhension = 1")
        self.listeBox_zones.pack(side=LEFT)
        #zone = self.listeBox_zones.curselection()

        self.button_draw_zone = Button(self.cadreZoneDessin, text="Tracer zone", command=self.draw_zone)
        self.button_draw_zone.pack(side=LEFT,padx=10,pady=10)

        self.button_effacer_zone = Button(self.cadreZoneDessin, text="Effacer  zones", command=self.delete_rect)
        self.button_effacer_zone.pack(side=LEFT,padx=10,pady=10)


    #-----------------cadre pour sauvegarder l'image de sortie--------------
        self.bouton_svg_img = Button(self.cadreSauvegarde, text="Générer et sauvegarder l'image", command=self.create_output_image)
        self.bouton_svg_img.pack(side=LEFT,padx=10,pady=10)

        self.bouton_next = Button(self.cadreSauvegarde,text='Image suivante', command=self.image_next)
        self.bouton_next.pack(side=LEFT,padx=10,pady=10)

        self.bouton_previous = Button(self.cadreSauvegarde,text='Image précédente', command=self.image_previous)
        self.bouton_previous.pack(side=LEFT,padx=10,pady=10)




    def load_multiple_files(self): #permet de charger plusieurs fichiers
        global liste_image
        global compteur
        global nbImages
        compteur = 0
        liste_image = askopenfilename(multiple=True)
        nbImages = len(liste_image)
        #Afficher les images dans une ListBox
        

        self.listeBox_nom_images = Listbox(self.cadreFichier,selectmode=SINGLE,width=25,height=3)
        for I in liste_image:
            self.listeBox_nom_images.insert(1, self.imageName(I))
        self.listeBox_nom_images.pack(side=LEFT)
        #Faire apparaitre un bouton pour utiliser une image de la ListBox
        self.utiliser_image =Button(self.cadreFichier, text="Utiliser image", command=self.use_image)
        self.utiliser_image.pack(side=LEFT,padx=10,pady=10)


    def Rechercher(self,texte,mot): #renvoie les indices des positions d'un mot dans un texte
        n=len(texte)
        m=len(mot)
        L=[]
        for i in range(n):
            # j=0
            if texte[i]==mot[0]:
                j=0
                compteur=0
                while j<m and texte[i]==mot[j]:
                    i+=1
                    j+=1
                    compteur+=1
                    # print(i,j)
                if compteur==m:
                    rang=i-compteur
                    L.append(rang)
        return(L)

    def imageName(self,pathImage):   #Permet d'obtenir le nom de l'image avec son chemin d'accès
        #print(os.getcwd())
        #print(pathImage)
        posDebutNom = self.Rechercher(pathImage,"/")[-1]+1
        posPoint = self.Rechercher(pathImage,".")[0]
        #print(posDebutNom)
        #print(posPoint)
        #print(len(pathImage))
        return(pathImage[posDebutNom:posPoint])


    def use_image(self):
        global finName
        finName = liste_image[self.listeBox_nom_images.curselection()[0]]
        if finName!="":
            self.label_image_name["text"]=self.imageName(finName)
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
        #self.coordsRect[0:2] = [event.x, event.y]
        global rect_red
        global rect_green
        if couleur == "green":
            self.coordsRect_green[0:2] = [event.x, event.y]
            rect_green = self.canvas.create_rectangle(self.coordsRect_green[0],self.coordsRect_green[1],self.coordsRect_green[0],self.coordsRect_green[1],outline = couleur, width = 3, fill = couleur, stipple='gray50')
            self.canvas.bind("<B1-Motion>", functools.partial(self.ajusterTaille, rectangle = rect_green, couleur = couleur, coordsRect = self.coordsRect_green))
        elif couleur == "red":
            self.coordsRect_red[0:2] = [event.x, event.y]
            rect_red = self.canvas.create_rectangle(self.coordsRect_red[0],self.coordsRect_red[1],self.coordsRect_red[0],self.coordsRect_red[1],outline = couleur, width = 3, fill = couleur, stipple='gray50')
            self.canvas.bind("<B1-Motion>", functools.partial(self.ajusterTaille, rectangle = rect_red, couleur = couleur, coordsRect = self.coordsRect_red))

    def ajusterTaille(self,event, rectangle, couleur,coordsRect): # se déclenche en maintenant clic gauche et en bougeant la souris
                                                        # pour tracer le rectangle
        self.canvas.coords(rectangle,coordsRect[0],coordsRect[1],event.x,event.y)
        self.canvas.bind('<ButtonRelease-1>', functools.partial(self.finirTrace, rectangle = rectangle, couleur = couleur, coordsRect = coordsRect))

    def finirTrace(self,event, rectangle, couleur, coordsRect): # se déclenche en relachant le clic gauche et termine le rectangle
        coordsRect[2:4] = [event.x,event.y]
        self.canvas.coords(coordsRect[0],coordsRect[1],coordsRect[2],coordsRect[3])
        #self.delete_rect(rectangle)
        
    def delete_rect(self):
        self.canvas.delete(rect_red)
        self.canvas.delete(rect_green)

    
    def draw_zone(self): #détermine la classe de la zone à tracer et la couleur du rectangle
        if self.listeBox_zones.curselection()[0]==0 :
            couleur = "red"
            zone_type = "forbidden"
            self.canvas.bind("<Button-1>", functools.partial(self.startTrace, couleur = couleur))
            rect_forbidden = self.coordsRect_red

        else:
            couleur = "green"
            zone_type = "authorized"
            self.canvas.bind("<Button-1>", functools.partial(self.startTrace, couleur = couleur))
            rect_authorized = self.coordsRect_green
        
    
#    def delete_zone(self): #supprime le dernier rectangle tracé
#        print("")
#        #à modifier
    
    def create_output_image(self): #créé et enregistre l'image de sortie avec les rectangle 1 et -1 sous le nom "nomImage.txt"
        #n,p=np.shape(self.image)[0:2]
        self.output_img = np.zeros(np.shape(self.image)[0:2])
        print("Rectangle vert : "+str(self.coordsRect_green))
        print("Rectangle rouge : "+str(self.coordsRect_red))


        #Les "+1" correspondent au rectangle vert, les "-1" au rectangle rouge
        self.output_img[self.coordsRect_green[1]:self.coordsRect_green[3],self.coordsRect_green[0]:self.coordsRect_green[2]] = 1
        self.output_img[self.coordsRect_red[1]:self.coordsRect_red[3],self.coordsRect_red[0]:self.coordsRect_red[2]] = -1

        #Enregistrement de l'image de sorite
        #posDebutNom = self.Rechercher(finName,os.getcwd())[0]+len(os.getcwd())+1
        #posPoint = self.Rechercher(finName,".")[0]
        #print(posDebutNom)
        #print(posPoint)
        #imageName=finName[posDebutNom:posPoint]
        np.savetxt(self.imageName(finName)+'.txt',self.output_img,fmt='%d')

        plt.figure()
        plt.imshow(self.output_img)
        plt.show()
    



    def image_next(self): #affiche l'image suivante dans l'interface graphique
        if self.listeBox_nom_images.curselection()[0]<nbImages:
            self.listeBox_nom_images.selection_set(self.listeBox_nom_images.curselection()[0]+1)
            self.listeBox_nom_images.selection_clear(self.listeBox_nom_images.curselection()[0])
            print(self.listeBox_nom_images.curselection()[0])
            self.use_image()

    
    def image_previous(self): #revient à l'image précédente dans l'interface graphique
        if self.listeBox_nom_images.curselection()[0]>0:
            self.listeBox_nom_images.selection_set(self.listeBox_nom_images.curselection()[0]-1)
            self.listeBox_nom_images.selection_clear(self.listeBox_nom_images.curselection()[0]+1)
            print(self.listeBox_nom_images.curselection()[0])
            self.use_image()
    



#Démarrage
fenetre=Interface()
fenetre.mainloop()

