# -*- coding utf8 -*-
#-------------------------------------------------------------------------------
# Nom du script    : Extraction_Arrondissements.py
# Objet            : Extraction des données géographiques délimitées par un
#                    ou plusieurs arrondissements
#
# Auteur           : Amina Barmani
#
# Objectif :
# Extraire des entités limitées à un ou plusieurs arrondissement(s) de Paris.
# Les entités extraites sont récupérées dans une nouvelle classe d'entités.
# Ce script est associé à deux outils scripts créés sur la géodatabase personelle 
#ArcGis
#-------------------------------------------------------------------------------

# Import des modules
import os
import arcpy

# Configuration de l'environnement de géotraitement
arcpy.env.overwriteOutput = 1

## Récupération des choix de l'utilisateur dans trois variables.
## Ces dernières pointent respectivement sur les trois paramètres
## d'un des deux outils script associé :

# - La variable fcIris doit contenir une string qui pointe sur la classe
#   d'entités des Iris sélectionnée par l'utilisateur. Le choix du/des
#   arrondissement(s) se fera à partir de de cette classe d'entités
fcIris = arcpy.GetParameterAsText(0)
# - La variable arrds doit contenir une string qui pointe sur le/les numéros
#   d'arrondissement sélectionné(s) par l'utilisateur. Les numéros
#   d'arrondissement sont lus à partir de la classe d'entités des Iris.
#   Ils sont ensuite afficher dynamiquement dans ce deuxième paramètre.
arrds  = arcpy.GetParameterAsText(1)
# - La variable fcIn doit contenir une string qui pointe sur la classe
#   d'entités choisie par l'utilisateur et qui va être découpée par l'emprise
#   d'un ou de chaque arrondissement généré par les entités iris sélectionnées.
fcIn   = arcpy.GetParameterAsText(2)


## traitement des données :

# Si un seul arrondissement est sélectionné, la boucle 'for' éxécutera
# l'extraction pour cette unique numéro d'arrondissement (arrd).

# Si plusieurs arrondissements sont sélectionnés, la boucle 'for' exécutera
# la même tâche pour chaque numéro d'arrondissement (arrd) trouvé entre
# chaque point-virgule dans la liste (arrds).

for arrd in arrds.split(";"):

    arcpy.AddMessage("\nArrondissement : {0}".format(arrd))
    fcOut = u"{0}\\{1}_{2}".format(os.path.split(fcIris)[0], os.path.split(fcIn)[1], arrd)
    arcpy.AddMessage("os.path.split(fcIris)[0] : {0}".format(os.path.split(fcIris)[0]))
    arcpy.AddMessage("os.path.split(fcIn)[1] : {0}".format(os.path.split(fcIn)[1]))

    arcpy.Select_analysis(fcIris, "arrd_Lyr", "DC = '{0}'".format(arrd))
    arcpy.Clip_analysis(fcIn, "arrd_lyr", fcOut)

arcpy.AddMessage("\n")