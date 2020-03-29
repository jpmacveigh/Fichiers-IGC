# -*- coding: utf-8 -*-
from LigneI import LigneI
from LigneB import LigneB
from LigneK import LigneK
from LigneJ import LigneJ
import time
import datetime
import os
import sqlite3
import boto3
from distanceOrthodromique import distanceOrthodromique
from capVitesse import capVitesse
from deltaCap import deltaCap
class FichierIGC:    # Un fichier IGC tel qu'il est fourni par un Oudie2 (par exemple)
    def __init__(self,path):   # constructeur à partir du path du ficier IGC
        #print ("nom du fichier igc : ",path)
        self.path=path
        self.fichierIgc = open(path,"r")   # ouverture du fichier IGC en lecture seule
        self.lignesB=[]
        self.lignesA=[]
        self.lignesH=[]
        self.lignesI=[]
        self.lignesJ=[]
        self.lignesG=[]
        self.lignesK=[]
        self.date="dd mm yy"
        for ligne in self.fichierIgc:           # itération sur toutes les lignes du ficheir IGC et on en teste le premier caractère
            ligne=ligne.replace("\n","")        # supression du caractère de fin de ligne
            if len(ligne) >0:                   # on ne traite pas les lignes vides, car j'en ai trouvé !
                if ligne[0].upper() == "A" :    # ligne A : première ligne obligatoire
                    self.lignesA.append(ligne)
                elif ligne[0].upper() == "H" : # lignes H : en-tête
                    self.lignesH.append(ligne)
                    if ligne[1:5].upper()=="FDTE":  # recherche de la date du vol
                        self.date=ligne[5:11]       # date du vol : ddmmyy
                elif ligne[0].upper() == "I" :  # ligne I : (optionnelle) Précise les compléments des lignesB (vitessse sol(gsp), true track(trt), etc.)
                    ligneI=LigneI(ligne)
                    if ligneI.isOK : self.lignesI.append(ligneI) # on ignore les ligneI mal formées
                elif ligne[0].upper() == "J" :  # ligne J : (optionnelle) Précise le contenu des lignesK
                    self.lignesJ.append(LigneJ(ligne))
                elif ligne[0].upper() == "B" :  # lignes B : les positions GPS (fix) à des heures régulièrement espacées
                    ligneB=None
                    if len(self.lignesI)!=0:
                        ligneB=LigneB(ligne,self.lignesI[0])
                    else:
                        ligneB=LigneB(ligne,LigneI("I000000000"))  # cas où il n'y a pas de ligneI
                    if ligneB.isOK : 
                        ligneB.date=self.date
                        self.lignesB.append(ligneB)   # on ignore les lignesB mal formées
                elif ligne[0].upper() == "G" :  # lignes G : informations de validation du fichier IGC
                    self.lignesG.append(ligne)
                elif ligne[0].upper() == "K" :  # lignes K : informations à des heures non régulières (wind direction (wdi), wind speed (wve), etc.)
                    if len(self.lignesJ)!=0:    #  on ignore les ligneK quand il n'existe pas de ligneJ
                        self.lignesK.append(LigneK(ligne,self.lignesJ[0]))
        self.fichierIgc.close()   # fermeture du fichier IGC
    
    def make_SQLITE3_file (self):
        ''' Fabrique une BD Sqlite3 avec toutes les positions du fichiers IGC '''
        (file_name,_)=os.path.splitext(self.path)
        path_sqlite3=file_name+".sqlite"  # la BD aura le même nom que le fichier igc avec l'extension sqlite
        print (path_sqlite3)
        conn=sqlite3.connect(path_sqlite3)      # creation de la base Sqlite3"
        conn.execute("DROP TABLE IF EXISTS positions")    # effacement puis re-céation de la table positions
        cmd="CREATE TABLE positions("
        cmd=cmd+"id_posi INT PRIMARY KEY,date TEXT,ts INTEGER,lati REAL,longi REAL,alti REAL,vz REAL, cap REAL,vit REAL,isLift TEXT)"
        conn.execute(cmd)
        i=0
        for ligne in self.lignesB :   # insertion des positions dans la table positions    
            if ligne.isOK and i> 0 :
                cmd=self.commande_insert(
                    "positions",
                    ["date","ts","lati","longi","alti","vz","cap","vit","isLift"],
                    ['"'+str(self.getDateTime(i))+'"',self.getTimeStamp(i),ligne.lat,ligne.long,ligne.gpsAlt,self.getVz(i),self.getCapVitesse(i)[0],self.getCapVitesse(i)[1],'"'+str(ligne.isLift)+'"'])
                conn.execute(cmd)
            i=i+1     
        conn.commit()
        conn.close()
        # stockage du fichier créé dans un bucket de AWS S3
        bucket_name="volavoile"
        s3 = boto3.resource('s3')
        #s3.Object(bucket_name,'newfile.txt').put(Body=content)
        s3.Object(bucket_name,'igc_tempo.sqite').put(Body=open(path_sqlite3,'rb'))


    
    def commande_insert(self,table_name,liste_champs,liste_valeurs):
        cmd='INSERT INTO '+table_name+' ('
        for champ in liste_champs:
            cmd=cmd+champ+','
        cmd=cmd[:-1]+') VALUES ('
        for valeur in liste_valeurs:
            cmd=cmd+str(valeur)+','
        cmd=cmd[:-1]+')'
        return (cmd)

    def getDateTime(self,rangLigneB):
        ''' retourne la date et heure UTC d'une position '''
        return datetime.datetime.fromtimestamp(self.getTimeStamp(rangLigneB))
    
    def getTimeStamp (self,rangLigneB):
        ''' retourne le timestamp d'une position '''
        return int(self.lignesB[rangLigneB].getTimeStamp())

    def getDeltaSecondes (self,rangLigneB):
        ''' retourne la durée écoulée (s) depuis la position précédante '''
        if (rangLigneB==0): return None
        else : return self.getTimeStamp(rangLigneB)- self.getTimeStamp(rangLigneB-1)
    
    def getVz(self,rangLigneB):
        ''' retourne la vitesse verticale (m/s) par rapport à la position précédante '''
        dt=self.getDeltaSecondes(rangLigneB)
        if dt==None : return None
        elif dt==0 : return None
        else :
            alt=self.lignesB[rangLigneB].gpsAlt
            altPrec=self.lignesB[rangLigneB-1].gpsAlt
            vz= (alt-altPrec)/dt
            return vz
    
    def getDistance(self,rangLigneB):
        ''' retourne la distance (m) parcourue depuis la position précedante '''
        if (rangLigneB==0):
            return None
        else :
            return distanceOrthodromique(self.lignesB[rangLigneB-1].long,self.lignesB[rangLigneB-1].lat,self.lignesB[rangLigneB].long,self.lignesB[rangLigneB].lat)
    
    def getCapVitesse(self,rangLigneB):
        ''' retourne le cap ]0,360] et vitesse (km/h) suivis depuis la position précédante '''
        dt=self.getDeltaSecondes(rangLigneB)
        if dt==None or dt==0: return(None,None)
        lon=self.lignesB[rangLigneB].long
        lonPrec=self.lignesB[rangLigneB-1].long
        lat=self.lignesB[rangLigneB].lat
        latPrec=self.lignesB[rangLigneB-1].lat
        rep=capVitesse(lonPrec,latPrec,lon,lat,dt)
        return rep
    
    def deltaCap(self,rangLigneB):
        ''' retourne la variation de cap [-180.,180.] depuis la position précédante '''
        assert rangLigneB in range(0,len(self.lignesB)), rangLigneB
        if (rangLigneB<2): return (None)
        (capBefore,_)=self.getCapVitesse(rangLigneB-1)
        (capAfter,_)=self.getCapVitesse(rangLigneB)
        return (deltaCap(capBefore,capAfter))
    
    def look_for_lift(self):
        res=[]
        deltat=240          # durée de la fenêtre temporelle (s)
        distance_test=1500  # distance minimale (m)
        lesLignes=[]    # les positions qui sont dans la fenêtre temporelle 
        lesLignes.append(self.lignesB[0])
        for ligne in self.lignesB:     # itération sur toutes les positions du fichiers
            lesLignes.append(ligne)   
            if (ligne.getTimeStamp()-lesLignes[0].getTimeStamp())>=deltat : # si on est à la fin de la fenêtre temporelle
                distance=distanceOrthodromique(lesLignes[0].long,lesLignes[0].lat,ligne.long,ligne.lat) # on calcule la distance parcourrue depuis l'entrée dans la fenêtre temporelle
                if distance <= distance_test : # on est dans une ascendance
                    res.append(ligne)
                    ligne.isLift=True
                    #ligne.affiche(["lat","long"])
                del lesLignes[0]  # on décalle la fenêtre d'une ligne
        print (len(res))
        return (res)       

    def affiche(self):
        #print (self.__dict__)
        print ("lignes A : ",len(self.lignesA))
        print ("lignes H : ",len(self.lignesH))
        print ("lignes I : ",len(self.lignesI))
        print ("lignes J : ",len(self.lignesJ))
        print ("lignes B : ",len(self.lignesB))
        print ("lignes K : ",len(self.lignesK))
        print ("lignes G : ",len(self.lignesG))
        print ("********* début du dictionnaire ***************")
        for k in sorted(self.__dict__):
            if (k=="lignesB"):
                print("nombre de positions :", len(self.__dict__[k]))
            else :
                print (k,self.__dict__[k])
        print ("********* fin du dictionnaire ***************")    