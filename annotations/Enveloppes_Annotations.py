# -*- coding utf-8 -*-

#------------------------------------------------------------------------------------------------
# Script : Enveloppes_Annotations.py
# Objet  : Récupération des rectangles englobants des annotations
#          et de leurs toponymes respectifs.
#------------------------------------------------------------------------------------------------

import arcpy, os

arcpy.env.overwriteOutput = True

inAC     = arcpy.GetParameterAsText(0) # inAC  (AC pour "Annotations Class")
champs   = arcpy.GetParameterAsText(1) # Liste des champs à garder de la classe d'annotations
outFC    = arcpy.GetParameterAsText(2) # outFC (FC pour "Features Class")

espT     = os.path.split(outFC)[0]     # espT (espace de Travail)
nomOutFC = os.path.split(outFC)[1]     # nom seul de la classe d'entités en sortie


# Création de la classe d'entités des emprises d'annotations (type "POLYGON")
# Le dernier argument attend une projection (facultatif); Cet argument peut récupérer
# la projection d'une classe d'entités existante (dans notre cas : inAC).
arcpy.CreateFeatureclass_management(espT, nomOutFC, "POLYGON", "", "", "", inAC)

# Ajout des champs cochés de la classe d'annotations dans la classe d'entités
listChamps = champs.split(";")
champsInAC = arcpy.ListFields(inAC)
for champ in champsInAC:
    if champ.name in listChamps:
        arcpy.AddMessage(champ.name)
        arcpy.AddField_management(outFC, champ.name, champ.type, champ.precision, champ.scale,
        champ.length, champ.aliasName, "", champ.required)

listChamps.insert(0, "Shape@")


# Ouverture d'un curseur de lecture ('sCursor') pour le jeton 'SHAPE@' (géométrie) et le champ
# 'TextString' de la table attributaire 'inAC' accessibles via le module 'da' ('data access')
with arcpy.da.SearchCursor(inAC, listChamps) as sCursor:

    # On ouvre 'outFC' pour insérer des lignes qui récupèreront la géométrie ('Shape@')
    # et le nom du toponyme de chaque annotation.
    with arcpy.da.InsertCursor(outFC, listChamps) as iCursor:

        # sCursor contient toutes les géométries (rectangles englobants : "Shape@")
        # et tous les toponymes ("TextString") de la table inAC (annotations).
        # On insert chaque ligne (row) de sCursor dans iCursor (table outFC).
        # Ainsi, à chaque tour de boucle dans sCursor, iCursor insère un enregistrement qui
        # récupère respectivement la géométrie et le toponyme contenu dans le row de sCursor.
        for row in sCursor:
            iCursor.insertRow(row)
