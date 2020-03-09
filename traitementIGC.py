import os
from FichierIGC import FichierIGC
'''
path="20140627 Saint-Auban 27 juin 2014 Discus 2b DP Copie de 46RXI0H1.igc"
fich= FichierIGC(path)
dateVol=fich.date
for i in range(len(fich.lignesB)):
.exit    heurePos=fich.lignesB[i].heureUTC
    print i,fich.getDateTime(fich.getTimeStamp(i)),fich.getDeltaSecondes(i),\
            fich.lignesB[i].lat,fich.lignesB[i].long,fich.getDistance(i),fich.getCapVitesse(i),fich.lignesB[i].pressAlt,fich.getVz(i)
'''

'''
dropboxpath= "J:/Dropbox/"              # PC fixe Baignerie
onedrivepath = "J:/OneDrive/"           # PC fixe Baignerie
'''

dropboxpath= "E:/Jean Pierre/Dropbox/"         # PC portable Lille
onedrivepath = "E:/Jean Pierre/OneDrive/"      # PC portable Lille

repertIGC=onedrivepath+"Vol a Voile/Fichiers igc degribes/"
os.chdir(repertIGC)

#basepath=onedrivepath+"Vol a voile\Positions.mdb"
basepath=onedrivepath+"Vol a voile/Positions.sqlite"
print ("path de la base Sqlite des vols produite : "+ basepath)
import sqlite3
conn = sqlite3.connect(basepath)      # ouverture de la base"

'''
import pypyodbc
repertBase=onedrivepath+"Vol a Voile/"
os.chdir(repertBase)
#pypyodbc.win_create_mdb("Positions.mdb")
conn = pypyodbc.win_connect_mdb("Positions.mdb")
'''
cur=conn.cursor()
cur.execute("DELETE from Positions")
#cur.execute("DROP TABLE Positions")
#cur.execute("CREATE TABLE Positions(idVol BLOB,date TEXT,heureUTC TEXT,latitude REAL,longitude REAL,altitude REAL)")
'''
cur.execute("CREATE TABLE Positions ( idVol VARCHAR(100), \
dateVol VARCHAR(6), \
heureUTC VARCHAR(6), \
t_stamp int, \
latitude float, \
longitude float, \
altitude float, \
Vz float, \
Cap float, \
Vit float);")
conn.commit()
'''

nbfich=0
nblignesB=0
#for path in os.listdir(repertIGC):
for i in range(5):
    path = os.listdir(repertIGC)[i]
    nbfich=nbfich+1
    print (nbfich)
    fich=FichierIGC(path)
    fich.affiche()
    numeroVol=path
    print ("nb de lignesB : ",len(fich.lignesB))
    if len(fich.lignesI)!=0:
        print ("nb de lignesI : ",len(fich.lignesI)," contenu : " ,fich.lignesI[0].ligneI)
    else:
        print ("nb de lignesI : ",len(fich.lignesI))
    print ("nb de lignesK : ",len(fich.lignesK))
    print ("date : ",fich.date)
    for i in range(len(fich.lignesB)):
        ligne= fich.lignesB[i]
        nblignesB=nblignesB+1
        dt=fich.getDeltaSecondes(i)
        distance=fich.getDistance(i)
        cap,vitesse = fich.getCapVitesse(i)
        cur.execute("INSERT INTO Positions (idVol,dateVol,heureUTC,t_stamp,latitude,longitude,altitude,Vz,Cap,Vit) \
        VALUES(?,?,?,?,?,?,?,?,?,?)",(numeroVol,fich.date,ligne.heureUTC,fich.getTimeStamp(i),ligne.lat,ligne.long,ligne.pressAlt,fich.getVz(i),cap,vitesse))
    conn.commit()
cur.close()
conn.close()
print ("nb fichiers traites :",nbfich)
print ("nb lignesB ajoutees :",nblignesB)
print ("nb moyen par fichier :", nblignesB/nbfich)
