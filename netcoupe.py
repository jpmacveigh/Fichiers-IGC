def anonymise(path_in,path_out):
  """
  Anonymise un fichier igc.
  """
  lines=[]
  with open (path_out,"w") as f_out: # on crée en écriture le fichier igc anonymisé
      with open (path_in,"r") as f_in : # on ouvre en lecture le fichier à anonymiser
          k=0
          try:
            lines=f_in.readlines() # on lit toutes les lignes du fichier igc d'origine
          except Exception as e : # si le fichier igc est mal formé, il est ignoré
            print (e)
            print ("f_in =",f_in)
            pass
          nblines=len(lines)
          if nblines > 0 :
            for line in lines:  # on boucle sur toutes les lignes di fichier igc d'origine
                if ((k >= 50 and k <= nblines-50) or line[0:5]=="HFDTE" or line[0:1]=='I' or line[0:1]=="J") : 
                    # On élimine les 50 premières et dernières lignes du fichier
                    # en retenant cependant la ligne qui débute débute par "HFDTE" qui indique la date du vol
                    # et les lignes  qui débutent par "I" ou"J" et qui sont nécéssaires au décodage des lignes qui commencent par "B" et
                    # qui donnent toutes les positions du vol.
                    f_out.write(line)  # on écrit la ligne dans le fichier new
                k=k+1 # on incrémente le compteur de lignes
          else :
            pass
import zipfile
import os
from datetime import datetime
print ("début du traitement à : ",str(datetime.now())) # impression de l'heure du début du traitement
compression = zipfile.ZIP_DEFLATED # paramètre de compression
#working_dir="J:\\Netcoupe\\"
working_dir="/Users/jeanpierremacveigh/Documents/Netcoupe/"
année="2010"
# Une fois les deux variables ci-dessus fixées, le programme va chercher et traiter
# le fichier IGC_Netcoupe"année".zip dans le répertoire "working_dir".
# Le résultat de l'anonymisation des ficheirs IGC sera placée
# dans le même répertoire dans le fichier IGC_Netcoupe"année"_new.zip"
# qui aura la même oranisation que le fichier zip iniial.
# Tous les ficheirs intermédiaires créés dans le "woring_dir" sont effacés à la fin du traitement.
# Le traitement d'un fichier annuel (2015) contenant environ 26500 fichiers igc doublement zipés (taille
# environ 2.4 Goctets) prend environ 30 minutes sur un MacBook Air M1 avec 16 Goctets de mémoire.
zip_in=working_dir+"IGC_NetCoupe"+année+".zip"  # Nom de l'archive zip initiale annuelle, de la forme "IGC_NetcoupeAAAA.zip" où AAAA est l'année. 
zip_out=working_dir+"IGC_NetCoupe"+année+"_new.zip"  # Nom de l'archive zip finale annuelle, de la forme "IGC_NetcoupeAAAA_new.zip" où AAAA est l'année. 
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
    name_in=working_dir+name.split("_")[1].split("/")[0]+"_"+name.split("/")[1].split(".")[0]+".igc"
    name_in=working_dir+name.split("_")[1].split("/")[0]+"_"+name.split("/")[1].split(".")[0]+".igc"
    name_out=name_in.split(".")[0]+"_new.igc"
    anonymise(name_in,name_out) # on anonymise le fichier igc
    os.remove(name_in) # on efface du working_dir le fichier igc initial    
    name_zip_igc=name.split("/")[1] # nom du zip qui contiendra le fichier igc anonymiser
    with zipfile.ZipFile(working_dir+name_zip_igc,"w") as zip_igc_out:
      zip_igc_out.write(name_out,arcname=name_out.split("/")[-1],compress_type=compression) # on zip le fichier igc anonymisé
    os.remove(name_out) # on efface du woring_dir le fichier igc anonymisé
zip_file_in.close()  # on ferme le fichier zip annuel initial
with zipfile.ZipFile(zip_out,"w") as zip_final: # on zip dans le fichier final tous les zip contenant un fichier anonymisé individuel
  list_des_zip=[file for file in os.listdir(working_dir) if file.split(".")[0].isdigit()]
  print ("Nombre de fichiers dans le zip final : ",len(list_des_zip))
  for zip in list_des_zip :
    zip_final.write(working_dir+zip,arcname=names[0]+zip,compress_type=compression)  
    os.remove(working_dir+zip) # on efface du working_dir le fichier zip contenant l'igc anoymisé
print ("fin du traitement à : ",str(datetime.now())) # impression de l'heure de fin du traitement