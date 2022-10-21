import zipfile
import os
def anonymise(path_in,path_out):
    print (path_in,path_out)
    with open (path_out,"w") as f_out: # on crée le fichier igc anonymisé
        with open (path_in) as f_in :
            k=0
            lines=f_in.readlines() # on lit toutes les lignes du fichier igc d'origine
            nblines=len(lines)
            for line in lines:  # on boucle sur toutes les lignes di fichier igc d'origine
                if ((k >= 50 and k <= nblines-50) or line[0:5]=="HFDTE" or line[0:1]=='I' or line[0:1]=="J") : 
                    # On ne retient que les lignes situées après la 50e ainsi que la ligne qui débute par "HFDTE" et décrit la date du vol
                    # et les lignes  qui débutent par "I" ou"J" et qui sont nécéssaires au décodage des lignes qui commencent par "B" et
                    # qui donnent toutes les positions du vol.
                    f_out.write(line)  # on écrit la ligne dans le fichier new
                k=k+1 # on incrémente le compteur de lignes
print (os.name)
if os.name == "posix":
    sep_dir="/"  # séparateur de répertoires pour Linux et MacOS
else:
    sep_dir="\\"  # séparateur de répertoires pour Windows
working_dir="J:\\Netcoupe"
#working_dir="/Users/jeanpierremacveigh/Documents/Netcoupe"
année="2015"
name_zip_in="IGC_NetCoupe"+année+".zip"
name_zip_out=name_zip_in.split(".")[0]+"_new.zip"
dir_name=working_dir+sep_dir+name_zip_in.split(".")[0] # le répertoire où sont extraits les fichiers zip
working_out_dir=working_dir+sep_dir+"Out"+sep_dir+name_zip_in.split(".")[0]
if not os.path.isdir(working_out_dir): os.makedirs(working_out_dir) # le répertoire où seront écrits les ficheirs anonymisés avant d'être rezipés
with zipfile.ZipFile(working_dir+sep_dir+name_zip_in,"r") as zip_in:  # dézipage du fichier NetcoupeAAAA.zip
    zip_in.extractall(working_dir)
list=os.listdir(dir_name)  # liste des fichiers dézipés (qui sont eux-même des fichiers zip)
print (len(list)) # nombre de fichiers dézipés
for file in list[:20] : # boucle sur les fichiers zip dézipés
    name_new=working_out_dir+sep_dir+file.split(".")[0]+"_new.igc"
    file_in=zipfile.ZipFile(dir_name+sep_dir+file).extract("NetCoupe"+année+"_"+file.split(".")[0]+".igc",path=working_out_dir) # extraction du fichier igc original
    anonymise(file_in,name_new) # anonymisation du fichier igc  
compression = zipfile.ZIP_DEFLATED
#with zipfile.ZipFile(working_dir+sep_dir+name_zip_out,"w") as zip_out: # création du fichiers zip qui contiendra les fichiers igc new
        #zip_out.write(name_zip_out,file.split(".")[0]+"_new.igc",compress_type=compression) # on zip le fichier igc anonymisé dans le zip final
    