# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------------------------
# Nom    : 03_Mutlitples_Txt_vers_multiples_Shp_directement.py
# Objet  : Création de polygones simples et/ou multi-parties vers autant de classes d'entités
#          que de fichiers textes contenant des coordonnées. Obligation d'exécuter le script
#          via un outil script créé dans ArcMap.
# -----------------------------------------------------------------------------------------------

# Accès au site-package arcpy pour ArcGis 10.xx, puis au module os pour gèrer
# les arborescences des fichiers et dossiers, et enfin au module codecs pour
# lire dans des fichiers texte avec gestion des caractères accentués.
import arcpy, os, codecs

# Configuration de l'environnement de géotraitement
arcpy.env.overwriteOutput = 1

# Variables globales
repTxt = arcpy.GetParameterAsText(0) # le répertoire des fichiers texte à traiter
inTxt  = arcpy.GetParameterAsText(1) # l'ensemble des fichiers texte à traiter

inTxt  = inTxt.replace("'", "")      # Suppression des éventuels simples quotes
for ficTxt in inTxt.split(";"):
    #ficTxt = ur"{}\\{}".format(repTxt, ficTxt) # Redéfinition du fichier texte avec son arborescence
    fcOut  = ficTxt.replace(".txt", ".shp")    # Classe d'entités à créer
    rep    = os.path.split(fcOut)[0]           # Arborescence du répertoire de travail
    nomFC  = os.path.split(fcOut)[1]           # Nom seul de la classe d'entités à créer
    prj    = 2154                              # Code du système de projection (RGF93)

    ficTxtR = codecs.open(ficTxt, "r", "utf8")

    listCoord = [] # Contiendra la liste des coordonnées d'une partie d'un polygone
    listPart  = [] # Contiendra le polygone simple ou en plusieurs parties
    listPlg   = [] # Contiendra tous les polygones simples ou en plusieurs parties

    numPoly = 0
    numPart = 0


    """-----------------------------------------------------------------------------
    PREMIÈRE PARTIE : Réorganisation des coordonnées du fichier texte dans listPlg
    dont la structure sous forme de liste sera bien reconnue et exploitée dans la
    seconde partie.
    """

    for ligne in ficTxtR.readlines():

        # --------------------------------------------------------------------------
        if "Polygone" in ligne or "Fin" in ligne or "\r\n" not in ligne:
            if numPoly != 0:
                listPart.append(listCoord)
                listPlg.append(listPart)
                listCoord = []
                listPart  = []

            numPoly += 1
            numPart = 0

        # --------------------------------------------------------------------------
        elif "Partie" in ligne or "Trou" in ligne:
            if numPart != 0:
                listPart.append(listCoord)
                listCoord = []

            numPart += 1
        # --------------------------------------------------------------------------
        elif "X" in ligne and "Y" in ligne:
            X = float(ligne.split(",")[0].replace("  X : ", "")) # Ajout du x
            Y = float(ligne.split(",")[1].replace(" Y : ", ""))  # Ajout du y
            listCoord.append([X, Y])

    ficTxtR.close()


    """-----------------------------------------------------------------------------
    SECONDE PARTIE : Création des polygones à partir de listPlg créée précédement.
    """

    # Création de la classe d'entités de type "POLYGONE"
    arcpy.CreateFeatureclass_management(rep, nomFC, "POLYGON", "", "", "", prj)

    point  = arcpy.Point() # Création d'un objet "Point"
    array  = arcpy.Array() # Création d'un premier objet "tableau"
    pArray = arcpy.Array() # Création d'un deuxième objet "tableau"

    # Ouverture en écriture de la nouvelle classe d'entités
    with arcpy.da.InsertCursor(fcOut, ["SHAPE@"]) as rows:

        for row in listPlg:        # Pour chaque entité (row) polygone...
            for part in row:       # ... et pour chaque partie de l'entité...
                for coord in part: # ... et pour chaque point de la partie (part):

                    point.X = coord[0] # Récupération du X dans l'objet "point"
                    point.Y = coord[1] # Récupération du Y dans l'objet "point"
                    array.add(point)   # Ajout du couple X,Y dans le tableau 'array'

                # Ajout du tableau "array" dans le tableau "pArray"
                pArray.add(array)
                # Vidage du tableau "array"
                array.removeAll()

            # Récupération de la structure géometrique de type polygone contenue
            # dans le tableau "pArray" et insertion de l'entité dans la table (rows)
            # de la classe d'entités (fcOut)
            rows.insertRow([arcpy.Polygon(pArray)])

            # Vidage du tableau "pArray"
            pArray.removeAll()

