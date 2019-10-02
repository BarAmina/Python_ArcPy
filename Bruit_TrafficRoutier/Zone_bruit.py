# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------
# Nom du script    : Zone_bruit.py
# Objet            : Génération de zones d'exposition au bruit du traffic routier
#-------------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Configuration de l'environnement de géotraitement
arcpy.env.overwriteOutput = True

# Paramétrage des données en entrée
iris = arcpy.GetParameterAsText(0)
rue = arcpy.GetParameterAsText(1)
# Paramétrage des données intermédiaires
rueBuffer = ur"{0}_buffer".format(rue)
irisClip = ur"{0}_clip".format(iris)

arcpy.AddMessage(u"Calcul du nombre d'habitants exposés au bruit...")

# Ajout d'un champ "Surface_complète" à la classe d'entités des IRIS
arcpy.AddField_management(iris, u"Surface_complète", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
# Renseignement du champ avec la surface de l'IRIS
arcpy.CalculateField_management(iris, u"Surface_complète", "[Shape_Area]", "VB", "")
arcpy.AddMessage(u"=> Calcul de la surface totale des IRIS OK")

# Ajout d'un champ "Distance" à la classe d'entités des rues
arcpy.AddField_management(rue, "Distance", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
# Renseignement du champ avec une portée du bruit, exprimée en mètres, variable suivant l'importance de la rue
arcpy.CalculateField_management(rue, "Distance", "Calc_Imp( !IMPORTANCE! )", "PYTHON", "def Calc_Imp(imp):\\n  if imp == '1':\\n    return 100\\n  elif imp == '2':\\n    return 50\\n  elif imp == '3':\\n    return 20\\n  else:\\n    return 0")
arcpy.AddMessage(u"=> Calcul de la portée du bruit de chaque rue OK")

# Création de zones tampons autour des rues avec les distances calculées
arcpy.Buffer_analysis(rue, rueBuffer, "Distance", "FULL", "ROUND", "ALL", "", "PLANAR")
arcpy.AddMessage(u"=> Création des zones d'exposition au bruit OK")

# Découpage des IRIS suivant les zones d'exposition au bruit
arcpy.Clip_analysis(iris, rueBuffer, irisClip, "")
arcpy.AddMessage(u"=> Découpage des IRIS suivant les zones d'exposition au bruit OK")

# Ajout d'un champ Pop_bruit à la classe d'analyse
arcpy.AddField_management(irisClip, "Pop_bruit", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
# Renseignement du champ avec la population des IRIS découpées
arcpy.CalculateField_management(irisClip, "Pop_bruit", "[P07_POP] / [Surface_complète] * [Shape_Area]", "VB", "")

arcpy.AddMessage(u"Calcul du nombre d'habitants exposés au bruit OK")
