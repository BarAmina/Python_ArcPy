# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------------------------
# Nom    : 01_Un_Txt_vers_un_Shape_directement.py
# Objet  : Création de polygones simples et/ou multi-parties vers une classe d'entités en partant
#          d'un fichier texte contenant des coordonnées. Obligation d'exécuter le script
#          via un outil script créé dans ArcMap.
#------------------------------------------------------------------------------------------------

import arcpy  # Accès au site-package arcpy (ArcGis 10.XXX)
import os     # Module pour la gestion des arborescences de fichier(s)
import codecs # Accès au codecs (caractères particuliers)

ficTxt  = arcpy.GetParameterAsText(0)
##ficTxt  = ur"D:\2018-2019\ArcGIS\Python_arcpy\Fomation python arcpy 2018-2019\Évaluation ING2_2018\Shapes_Texte\Shape_01.txt"
listTxt = codecs.open(ficTxt, "r", "utf8")
rep     = os.path.split(ficTxt)[0]
fcOut   = ficTxt.replace(".txt", ".shp")
nomFC   = os.path.split(fcOut)[1]
prj     = 2154 # Code du système de coordonnées projetées (RGF93-Lambert93)

arcpy.CreateFeatureclass_management(rep, nomFC, "POLYGON", "", "", "", prj)

with arcpy.da.InsertCursor(fcOut, ["SHAPE@"]) as rows:

    point  = arcpy.Point()
    array  = arcpy.Array()
    pArray = arcpy.Array()

    numPoly = 0
    numPart = 0

    for ligne in listTxt.readlines():

        # ----------------------------------------------------------------------
        if "Polygone" in ligne:
            if numPoly != 0:
                pArray.add(array)
                polygon = arcpy.Polygon(pArray)
                rows.insertRow([polygon])
                array.removeAll()
                pArray.removeAll()

            numPoly += 1

        # ----------------------------------------------------------------------
        elif "Partie" in ligne or "Trou" in ligne:
            if numPart != 0:
                pArray.add(array)
                array.removeAll()

            numPart += 1

        # ----------------------------------------------------------------------
        elif "X" in ligne and "Y" in ligne:
            point.X = float(ligne.split(",")[0].replace("  X : ", ""))
            point.Y = float(ligne.split(",")[1].replace(" Y : ", ""))
            array.add(point)

    pArray.add(array)
    polygon = arcpy.Polygon(pArray)
    rows.insertRow([polygon])
    array.removeAll()
    pArray.removeAll()

listTxt.close()