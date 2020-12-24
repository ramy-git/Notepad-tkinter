import tkinter as tk
from tkinter import ttk
from tkinter import font, colorchooser, filedialog
from tkinter import messagebox
from tkinter.filedialog import *


class Editeur(tk.Frame):
    App = tk.Tk()

    # On importe nos icones ici ( situé dans le fichier icones)

    icone_nouveau_fichier = tk.PhotoImage(file="icones/new.png")
    icone_ouvrir = tk.PhotoImage(file="icones/open.png")
    icone_enregistrer = tk.PhotoImage(file="icones/save.png")
    icone_enregistrer_sous = tk.PhotoImage(file="icones/save_as.png")
    icone_quitter = tk.PhotoImage(file="icones/exit.png")
    icone_rechercher = tk.PhotoImage(file="icones/find.png")

    ###color theme
    def __init__(self, **kw):

        super().__init__(**kw)
        self.App.geometry('1200x720')  # on initialise avec une definition de 1280x720 pixel
        self.App.title('Sans titre- Bloc-note') #on initialise le nom par default du titre de la fenetre
        self.App.wm_iconbitmap("icones/notepadicn.ico")

        #*** On definit le menu principal ( la barre en haut contenant les sous-enu de fichier, outils et d'aide
        self.menuPrincipal = Menu()
        self.App.config(menu=self.menuPrincipal)
        self.fichier = Menu(self.menuPrincipal, tearoff=0)
        self.outils = tk.Menu(self.menuPrincipal, tearoff=0)
        self.aideMenu = Menu(self.menuPrincipal, tearoff=0)
        self.couleurTheme = Menu(self.menuPrincipal, tearoff=0)
        self.menuPrincipal.add_cascade(label="Fichier", menu=self.fichier)
        self.menuPrincipal.add_cascade(label="Outils", menu=self.outils)
        self.menuPrincipal.add_cascade(label="Themes", menu=self.couleurTheme)
        self.menuPrincipal.add_cascade(label="Aide", menu=self.aideMenu)

        # par rapport au theme et au couleur de l'arriere plan et du premier plan
        self.choixTheme = StringVar()
        self.icone_default = tk.PhotoImage(file="icones/default.png")
        self.icone_doublegris = tk.PhotoImage(file="icones/doublegris.png")
        self.icone_sombre = tk.PhotoImage(file="icones/sombre.png")
        self.icone_vert_bleu = tk.PhotoImage(file="icones/vert_bleu.png")


        self.couleur_theme_icones = (
            self.icone_default, self.icone_doublegris, self.icone_sombre, self.icone_vert_bleu, )

        self.listeTheme = {
            "Par default": ("#000000", "#ffffff"),
            "Gris": ("#333333", "#C0C0C0"),
            "Sombre": ("#c4c4c4", "#2d2d2d"),
            "Vert Bleu": ("#00FF00", "#447CF4")
             }

        # ***************************Barre d'outils************************************
        self.barre_outils = Label(self.App)
        self.barre_outils.pack(side=tk.TOP, fill=tk.X)

        # on cree la boite pour les modifications sur la police
        self.tuplePolice = font.families()
        self.typePolice = StringVar()
        self.boitePolice = ttk.Combobox(self.barre_outils, width=30, textvariable=self.typePolice, state="readonly")
        self.boitePolice["values"] = self.tuplePolice
        self.boitePolice.current(self.tuplePolice.index("Arial"))
        self.boitePolice.grid(row=0, column=0, padx=5)

        # boite pour regler la taille de la police
        self.taille_var = tk.IntVar()
        self.taillePolice = ttk.Combobox(self.barre_outils, width=14, textvariable=self.taille_var, state="readonly")
        self.taillePolice["values"] = tuple(range(8, 80, 2))
        self.taillePolice.current(4)
        self.taillePolice.grid(row=0, column=1, padx=5)

        # #bold button
        self.iconeGras = tk.PhotoImage(file="icones/bold.png")
        self.boutonGras = ttk.Button(self.barre_outils, image=self.iconeGras)
        self.boutonGras.grid(row=0, column=2, padx=5)

        # #italic button
        self.iconeItal = tk.PhotoImage(file="icones/italic.png")
        self.boutonItal = ttk.Button(self.barre_outils, image=self.iconeItal)
        self.boutonItal.grid(row=0, column=3, padx=5)

        # #bouton pour souligner
        self.iconeSouligne = tk.PhotoImage(file="icones/underline.png")
        self.boutonSouligne = ttk.Button(self.barre_outils, image=self.iconeSouligne)
        self.boutonSouligne.grid(row=0, column=4, padx=5)

        # #bouton pour souligner la oculeur de la police
        self.icone_couleur_police = tk.PhotoImage(file="icones/font_color.png")
        self.boutonCouleurPolice = ttk.Button(self.barre_outils, image=self.icone_couleur_police)
        self.boutonCouleurPolice.grid(row=0, column=5, padx=5)

        # #bouton pour la fonction rechercher (loupe)
        self.iconeFind = tk.PhotoImage(file="icones/find.png")
        self.boutonLoupe = ttk.Button(self.barre_outils, image=self.iconeFind)
        self.boutonLoupe.grid(row=0, column=6, padx=5)

        # ***************************INIT DE LA ZONE DE TEXTE************************************
        self.zoneTexte = tk.Text(self.App)
        self.zoneTexte.config(wrap="word", relief=tk.FLAT)

        self.barreDefil = tk.Scrollbar(self.App) # la barre de defilement est initiliase ici et ajouter à la fenetre
        self.zoneTexte.focus_set() #Si l’application qui contient le widget appelant a le focus, le focus est dirigé vers ce widget.
                                    # Sinon, Tk le donnera au widget lorsque l’application aura le focus à nouveau.

        self.barreDefil.pack(side=tk.RIGHT, fill=tk.Y)
        self.zoneTexte.pack(fill=tk.BOTH, expand=True)
        self.barreDefil.config(command=self.zoneTexte.yview)
        self.zoneTexte.config(yscrollcommand=self.barreDefil.set)

        # On regle les parametre par default pour la police

        self.typePolice_actuel = "Arial"
        self.taillePolice_actuel = "16"
        self.boitePolice.bind("<<ComboboxSelected>>", self.changerPolice)
        self.taillePolice.bind("<<ComboboxSelected>>", self.modifierTaillePolice)

        # On attribue les fonctions aux boutons
        self.boutonGras.configure(command=self.enGras)
        self.boutonItal.configure(command=self.enItalique)
        self.boutonSouligne.configure(command=self.enSouligne)
        self.boutonLoupe.configure(command=self.fonctionRechercher)
        self.boutonCouleurPolice.configure(command=self.changerCouleurPolice)

        self.zoneTexte.configure(font=("Arial", 16))

        self.url = ""
        # *** on ajoute les commandes au menu de gestion des fichiers
        self.fichier.add_command(label="Nouveau", image=self.icone_nouveau_fichier, compound=tk.LEFT, command=self.nouveau_fichier)
        self.fichier.add_command(label="Ouvrir", image=self.icone_ouvrir, compound=tk.LEFT, command=self.ouvrir_fichier)
        self.fichier.add_command(label="Sauvegarder", image=self.icone_enregistrer, compound=tk.LEFT, command=self.enregistrer)
        self.fichier.add_command(label="Sauevgarder sous", image=self.icone_enregistrer_sous, compound=tk.LEFT,
                                 command=self.enregistrer_sous)
        self.fichier.add_command(label="Quitter", image=self.icone_quitter, compound=tk.LEFT, command=self.quitter)

        # *** on ajoute les commandes au menu d'outils
        self.outils.add_command(label="Copier", compound=tk.LEFT,
                                command=lambda: self.zoneTexte.event_generate("<Control c>"))
        self.outils.add_command(label="Coller", compound=tk.LEFT,
                                command=lambda: self.zoneTexte.event_generate("<Control v>"))
        self.outils.add_command(label="Couper", compound=tk.LEFT,
                                command=lambda: self.zoneTexte.event_generate("<Control x>"))
        self.outils.add_command(label="Tout effacer", compound=tk.LEFT,
                                command=lambda: self.zoneTexte.delete(1.0, tk.END))

        # *** on ajoute les commandes au menu d'aide
        self.aideMenu.add_command(label="A propos", compound=tk.LEFT, command=self.__showAbout)

        # On lance une boucle qui va creer tout les boutons pour chaque theme
        count = 0
        for i in self.listeTheme:
            self.couleurTheme.add_radiobutton(label=i, image=self.couleur_theme_icones[count], variable=self.choixTheme,
                                              compound=tk.LEFT,
                                              command=self.changerTheme)
            count += 1

        #### FIN DU INIT ###
        ### DEBUT DES FONCTIONS ###
    ###### OPERATION SUR LA POLICE  ############


    def changerPolice(App, type):

        App.typePolice_actuel = App.typePolice.get()

        App.typePolice_actuel = App.typePolice.get()
        App.zoneTexte.configure(font=(App.typePolice_actuel, App.taillePolice_actuel))

    def modifierTaillePolice(App, taille):

        App.taillePolice_actuel = App.taille_var.get()
        App.zoneTexte.configure(font=(App.typePolice_actuel, App.taillePolice_actuel))

        #FONCTIONS DES BOUTONS SUR LA POLICE
    # #FONCTION QUI MET LE TEXTE EN GRAS
    def enGras(self):
        text_property = tk.font.Font(font=self.zoneTexte["font"])
        if text_property.actual()["weight"] == "normal":
            self.zoneTexte.configure(font=(self.typePolice_actuel, self.taillePolice_actuel, "bold"))
        if text_property.actual()["weight"] == "bold":
            self.zoneTexte.configure(font=(self.typePolice_actuel, self.taillePolice_actuel, "normal"))

    # #FONCTION QUI MET LE TEXTE EN ITALIQUE
    def enItalique(self):
        text_property = tk.font.Font(font=self.zoneTexte["font"])
        if text_property.actual()["slant"] == "roman":
            self.zoneTexte.configure(font=(self.typePolice_actuel, self.taillePolice_actuel, "italic"))
        if text_property.actual()["slant"] == "italic":
            self.zoneTexte.configure(font=(self.typePolice_actuel, self.taillePolice_actuel, "normal"))

    # #FONCTION QUI SOULIGNE LE TEXTE
    def enSouligne(self):
        text_property = tk.font.Font(font=self.zoneTexte["font"])
        if text_property.actual()["underline"] == 0:
            self.zoneTexte.configure(font=(self.typePolice_actuel, self.taillePolice_actuel, "underline"))
        if text_property.actual()["underline"] == 1:
            self.zoneTexte.configure(font=(self.typePolice_actuel, self.taillePolice_actuel, "normal"))

    # #FONCTION QUI CHANGE LA COULEUR DE LA POLICE
    def changerCouleurPolice(self):
        couleur_variable = tk.colorchooser.askcolor()

        self.zoneTexte.configure(fg=couleur_variable[1])

    def changerTheme(self):
        themeChoisi = self.choixTheme.get()
        color_tuple = self.listeTheme.get(themeChoisi)
        fg_color, bg_color = color_tuple[0], color_tuple[1]
        self.zoneTexte.config(background=bg_color, fg=fg_color)


        ###### FONCTION SUR LES ENREGISTREMENT ET OUVERTURE DE FICHIER
        #*************************************************************
    def nouveau_fichier(self, Event=None):
        global url
        url = ""
        self.zoneTexte.delete(1.0, tk.END)

    def ouvrir_fichier(self, Event=None):
        global url
        url = filedialog.askopenfilename(initialdir=os.getcwd(), title="Choisissez un fichier",
                                         filetypes=(("Fichier texte", "*.txt"), ("Tous les fichiers", "*.*")))
        try:
            with open(url, "r") as fr:
                self.zoneTexte.delete(1.0, tk.END)
                self.zoneTexte.insert(1.0, fr.read())
        except FileNotFoundError:
            return
        except:
            return
        self.App.title(os.path.basename(url)) # on change le titre de la fenetre pour le faire correspondre à celui du fichier

    # pour sauvegarder
    def enregistrer(self, Event=None):
        global url
        try:
            if url:
                content = str(self.zoneTexte.get(1.0, tk.END))
                with open(url, "w", encoding="utf-8") as fw:
                    fw.write(content)
            else:
                url = filedialog.asksaveasfile(mode="w", defaultextension=".txt",
                                               filetypes=(("Fichier texte", "*.txt"), ("Tous les fichiers", "*.*")))
                content2 = self.zoneTexte.get(1.0, tk.END)
                url.write(content2)
                url.close()
        except:
            return

    # save as functionality
    def enregistrer_sous(self, Event=None):
        global url
        try:

            content = self.zoneTexte.get(1.0, tk.END)

            url = filedialog.asksaveasfile(mode="w", defaultextension=".txt",
                                           filetypes=(("Fichier texte", "*.txt"), ("Tous les fichiers", "*.*")))

            url.write(content)
            url.close()
        except:
            return

    def quitter(self, Event=None):
        self.destroy()


    ### FONCTION RECHERCHER ET REMPLACER #####
    #*****************************************
    def fonctionRechercher(self, Event=None):

        def find():
            mot = inputRecherche.get()
            self.zoneTexte.tag_remove("match", "1.0", tk.END)
            matches = 0
            if mot:
                positionDebut = "1.0"
                while True:
                    positionDebut = self.zoneTexte.search(mot, positionDebut, stopindex=tk.END)
                    if not positionDebut:
                        break
                    positionFin = f"{positionDebut}+{len(mot)}c"
                    self.zoneTexte.tag_add("match", positionDebut, positionFin)
                    matches += 1
                    positionDebut = positionFin
                    self.zoneTexte.tag_config("match", foreground="red",
                                              background="yellow")  # le resultat de la recherche est surligne en rouge sur fond jaune

        def replace():
            mot = inputRecherche.get()
            texte_remplacement = inputRemplace.get()
            contenu = self.zoneTexte.get(1.0, tk.END)
            new_contenu = contenu.replace(mot, texte_remplacement)
            self.zoneTexte.delete(1.0, tk.END)
            self.zoneTexte.insert(1.0, new_contenu)

        boiteLoupe = tk.Toplevel()
        boiteLoupe.geometry("350x150")
        boiteLoupe.title("La Loupe")
        boiteLoupe.resizable(0, 0)

        # frame (= cadre) Un cadre est simplement un conteneur pour d’autre widgets.
        frameLoupe = ttk.LabelFrame(boiteLoupe, text="Chercher/Remplacer")
        frameLoupe.pack(pady=20)
        # labels (= etiquette) servent à afficher une ou plusieurs lignes de texte avec le même style
        texteRechercheLabel = ttk.Label(frameLoupe, text="Expression a rechercher : ")
        texteRemplaceLabel = ttk.Label(frameLoupe, text="Remplacer par: ")
        # les input
        inputRecherche = ttk.Entry(frameLoupe, width=30)
        inputRemplace = ttk.Entry(frameLoupe, width=30)
        # initialisation des boutons
        boutonRecherche = ttk.Button(frameLoupe, text="Chercher", command=find)
        boutonRemplace = ttk.Button(frameLoupe, text="Remplacer", command=replace)
        # grilel des label  (leur position spatial)
        texteRechercheLabel.grid(row=0, column=0, padx=4, pady=4)
        texteRemplaceLabel.grid(row=1, column=0, padx=4, pady=4)
        # les grille pour les input (leur position spatial)
        inputRecherche.grid(row=0, column=1, padx=4, pady=4)
        inputRemplace.grid(row=1, column=1, padx=4, pady=4)
        # les grilles pour les boutons (leur position spatial)
        boutonRecherche.grid(row=2, column=0, padx=8, pady=4)
        boutonRemplace.grid(row=2, column=1, padx=8, pady=4)

        boiteLoupe.mainloop()



    def __showAbout(self):
        tk.messagebox.showinfo("A propos", "Version :1.0")

    def main(self):

        # mainloop pour que la fenetre reste ouverte en boucle jusqu'a sa destruciton
        self.App.mainloop()

    # Run main application


if __name__ == "__main__":
    newFenetre = Editeur()
    newFenetre.main()

else:
    print("Erreur dans le main")
