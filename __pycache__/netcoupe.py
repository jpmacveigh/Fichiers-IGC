def anonymise(path_in,path_out):
    #print (path_in,path_out)
    lines=[]
    with open (path_out,"w") as f_out: # on crée le fichier igc anonymisé
        with open (path_in,"r") as f_in :
            k=0
            try:
              lines=f_in.readlines() # on lit toutes les lignes du fichier igc d'origine
            except Exception as e :
              print (e)
              print ("f_in =",f_in)
              pass
            nblines=len(lines)
            if nblines > 0 :
              for line in lines:  # on boucle sur toutes les lignes di fichier igc d'origine
                  if ((k >= 50 and k <= nblines-50) or line[0:5]=="HFDTE" or line[0:1]=='I' or line[0:1]=="J") : 
                      # On ne retient que les lignes situées après la 50e ainsi que la ligne qui débute par "HFDTE" et décrit la date du vol
                      # et les lignes  qui débutent par "I" ou"J" et qui sont nécéssaires au décodage des lignes qui commencent par "B" et
                      # qui donnent toutes les positions du vol.
                      f_out.write(line)  # on écrit la ligne dans le fichier new
                  k=k+1 # on incrémente le compteur de lignes
            else :
              pass
import zipfile
import os
from datetime import datetime
print ("début du traitement à : ",str(datetime.now()))
print (os.name)
if os.name == "posix":
    sep_dir="/"  # séparateur de répertoires pour Linux et MacOS
else:
    sep_dir="\\"  # séparateur de répertoires pour Windows
compression = zipfile.ZIP_DEFLATED
#perm_working_dir="/content/drive/MyDrive/Colab Notebooks/Vol à voile/"
#perm_working_dir="J:\\Netcoupe\\"
perm_working_dir="/Users/jeanpierremacveigh/Documents/Netcoupe/"
#tempo_working_dir="/content/"
tempo_working_dir=perm_working_dir
année="2015"
zip_in=perm_working_dir+"IGC_NetCoupe"+année+".zip"  # Nom de l'archive zip initiale annuelle, de la forme "IGC_NetcoupeAAAA.zip" où AAAA est l'année. 
zip_out=perm_working_dir+"IGC_NetCoupe"+année+"_new.zip"  # Nom de l'archive zip finale annuelle, de la forme "IGC_NetcoupeAAAA_new.zip" où AAAA est l'année. 
zip_file_in=zipfile.ZipFile(zip_in, mode='r') # Ouverture de l'archive zip initiale
names=zip_file_in.namelist() # liste de tous les fichiers présents dans l'archive zip initiale
print ("Nombre de fichiers dans le zip initial : ", len(names)-1)
for name in names: # Boucle sur tous les igc contenus dans l'archvive initiale
  if name[-1] != "/" : # on saute le premier qui est un répertoire
    #print(name)
    igc_zip_in=zip_file_in.extract(name,path=perm_working_dir) # on extrait le fichier zipé qui contient l'igc
    try:
      zipfile.ZipFile(igc_zip_in,mode="r").extractall(path=perm_working_dir) # on le dézipe pour accéder à l'unique igc qu'il contient
    except Exception as e :
      print (e)
      print ("igc_zip_in =",igc_zip_in)
      continue
    name_in=tempo_working_dir+name.split("_")[1].split("/")[0]+"_"+name.split("/")[1].split(".")[0]+".igc"
    name_in=tempo_working_dir+name.split("_")[1].split("/")[0]+"_"+name.split("/")[1].split(".")[0]+".igc"
    name_out=name_in.split(".")[0]+"_new.igc"
    anonymise(name_in,name_out) # on anonymise le fichier igc
    os.remove(name_in) # on efface le fichier igc initial
    # on zip le fichier igc anonymisé :
    name_zip_igc=name.split("/")[1] # nom du zip qui contiendra le fichier igc anonymiser
    with zipfile.ZipFile(tempo_working_dir+name_zip_igc,"w") as zip_igc_out:
      zip_igc_out.write(name_out,arcname=name_out.split("/")[-1],compress_type=compression)
    os.remove(name_out) # on efface le fichier igc anoymisé
zip_file_in.close()  # on ferme le fichier zip annuel initial
with zipfile.ZipFile(zip_out,"w") as zip_final: # on zip dans le fichier final tous les zip contenant un fichier anonymisé individuel
  list_des_zip=[file for file in os.listdir(tempo_working_dir) if file.split(".")[0].isdigit()]
  print ("Nombre de fichiers dans le zip final : ",len(list_des_zip))
  for zip in list_des_zip :
    zip_final.write(tempo_working_dir+zip,arcname=names[0]+zip,compress_type=compression)  
    os.remove(tempo_working_dir+zip) # on efface le fichier zip contenant l'igc anoymisé
print ("fin du traitement à : ",str(datetime.now()))