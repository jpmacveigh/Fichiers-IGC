import zipfile
import os
from datetime import datetime
from FichierIGC import FichierIGC
from Terrains import Terrains
import json
def analyseMaxiAltitude(path,write=True):
    """
    Recherche le jour, le terrain de décollage et l'altitude maximale atteinte par un vol
    """
    flight=FichierIGC(path)
    if flight.isOK:
        maximum=flight.getAltitudeMaxi()
        decollage=flight.positionTakeOff()
        nearest=terrains.nearestTerrain(decollage.long,decollage.lat)
        print(decollage.date,decollage.heureUTC,nearest[0],nearest[1][1],maximum[0].date,maximum[0].heureUTC,maximum[1])
        if write :
            file.write(json.dumps({
                "path":path.split("\\")[-1],
                "dec_date":decollage.date,
                "dec_heure":decollage.heureUTC,
                "nearest_dist":nearest[0],
                "nearest":nearest[1][1],
                "maxi_date":maximum[0].date,
                "maxi_heure":maximum[0].heureUTC,
                "maxi_longi":maximum[0].long,
                "maxi_lati":maximum[0].lat,
                "altiMax":maximum[1]
            })+"\n")

print ("début du traitement à : ",str(datetime.now())) # impression de l'heure du début du traitement
#working_dir="J:\\Netcoupe\\"
working_dir="/Users/jeanpierremacveigh/Documents/Netcoupe/"
année="2016"
# Une fois les deux variables ci-dessus fixées, le programme va chercher et traiter
# le fichier IGC_Netcoupe"année".zip dans le répertoire "working_dir".
zip_in=working_dir+"Retour_Fred_IGC_NetCoupe"+année+"_new.zip"  # Nom de l'archive zip initiale annuelle, de la forme "IGC_NetcoupeAAAA.zip" où AAAA est l'année. 
zip_file_in=zipfile.ZipFile(zip_in, mode='r') # Ouverture de l'archive zip initiale
names=zip_file_in.namelist() # liste de tous les fichiers présents dans l'archive zip initiale
print ("Nombre de fichiers dans le zip initial : ", len(names)-1)
for name in names: # Boucle sur tous les igc contenus dans l'archvive initiale
  if name[-1] != "/" : # on saute le premier qui est un répertoire
    #print(name)
    igc_zip_in=zip_file_in.extract(name,path=working_dir) # on extrait le fichier zipé qui contient l'igc
    try:
      zipfile.ZipFile(igc_zip_in,mode="r").extractall(path=working_dir) # on le dézipe pour accéder à l'unique igc qu'il contient
    except Exception as e :  # si le zip est incorrect, il sera ignoré
      print (e)
      print ("igc_zip_in =",igc_zip_in)
      continue
    name_in=working_dir+"netcoupe/"+name.split("_")[1].split("/")[0]+"_"+name.split("/")[1].split(".")[0]+".igc"
    name_out=name_in.split(".")[0]+"_new.igc"
    #print (name_out)
zip_file_in.close()  # on ferme le fichier zip annuel initial
print ("fin du dézipage des fichiers igc à : ",str(datetime.now())) # impression de l'heure de fin du traitement
terrains=Terrains()
file=open(working_dir+"maximums_après_anonymisation.txt","w")
dir_igc=working_dir+"netcoupe/"
liste_des_igc=sorted(os.listdir(dir_igc))
print ("nombre de fichiers igc dézipés =",len(liste_des_igc))
for igc in liste_des_igc :
    analyseMaxiAltitude(dir_igc+igc,write=True) # on analyse le fichier igc 
print ("fin du traitement des fichiers igc à : ",str(datetime.now()))