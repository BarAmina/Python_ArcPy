# -*- coding: utf-8 -*-

##------------------------------------------------------------------------------
## Auteur : Barmani Amina
## Objet  : Calcul de populations autour d'entités ponctuels
##          selon une zone d'influence définie par l'utilisateur.
## Date   : 05/09/2019
##------------------------------------------------------------------------------

# Import des modules standards
import os
# Import du module arcpy
import arcpy

# Configuration de l'environnement de géotraitement
arcpy.env.overwriteOutput = 1

# Déclaration des données en entrée
iris = arcpy.GetParameterAsText(0)
proposition = arcpy.GetParameterAsText(1)
distance = arcpy.GetParameterAsText(2)
# Déclaration des données en entrée
statistiqueClient = arcpy.GetParameterAsText(3)
# Déclaration des données intermédiaires
propositionBuffer = "{0}_Buffer".format(proposition)
propositionBufferIntersect = "{0}_Buffer_Intersec".format(proposition)


# Création de zones tampons autour des propositions d'implantation
arcpy.Buffer_analysis(proposition, propositionBuffer, "{0} Meters".format(distance), "FULL", "ROUND", "LIST", "Nom", "PLANAR")
arcpy.AddMessage("Création de zones tampons autour des propositions d'implantation")

# Calcul de la surface des IRIS
arcpy.AddField_management(iris, "Surf_iris_Totale", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.CalculateField_management(iris, "Surf_iris_Totale", "[Shape_Area]", "VB", "")
arcpy.AddMessage("Calcul de la surface des IRIS")

# Création de zones à l' intersection des zones tampons et des IRIS
arcpy.Intersect_analysis("{0} #;{1} #".format(propositionBuffer, iris), propositionBufferIntersect, "ALL", "", "INPUT")
arcpy.AddMessage("Création de zones de zones à l' intersection des zones tampons et des IRIS")

# Calcul du nombre potentiel de clients dans ces zones
arcpy.AddField_management(propositionBufferIntersect, "Nb_Clients_Potentiels", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.CalculateField_management(propositionBufferIntersect, "Nb_Clients_Potentiels", "([P07_POP1117] + [P07_POP1824]) / [Surf_iris_Totale] * [Shape_area]", "VB", "")
arcpy.AddMessage("Calcul du nombre potentiel de clients dans ces zones")

# Agrégation du nombre potentiel de clients pour chaque proposition d'implantation
arcpy.Statistics_analysis(propositionBufferIntersect, statistiqueClient, "Nb_Clients_Potentiels SUM", "Nom")
arcpy.AddMessage("Agrégation du nombre potentiel de clients pour chaque proposition d'implantation")

# Supppression des données intermédiaires
arcpy.Delete_management(propositionBuffer)
arcpy.Delete_management(propositionBufferIntersect)
