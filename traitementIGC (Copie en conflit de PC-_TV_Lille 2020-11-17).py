# -*- coding: utf8 -*-
import os
import datetime
import time
from distanceOrthodromique import distanceOrthodromique
from capVitesse import capVitesse
class FichierIGC:
    def __init__(self,path):
        print "nom du fichier igc : ",path
        self.fichierIgc = open(path,"r")
        self.lignesB=[]
        self.lignesA=[]
        self.lignesH=[]
        self.lignesI=[]
        self.lignesJ=[]
        self.lignesG=[]
        self.lignesK=[]
        self.date="dd mm yy"
        for ligne in self.fichierIgc:
            ligne=ligne.replace("\n","")
            if len(ligne) >0:                   # on ne traite pas les lignes vides. Car j'en ai trouvé !
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
                    if ligneB.isOK : self.lignesB.append(ligneB)   # on ignore les lignesB mal formées
                elif ligne[0].upper() == "G" :  # lignes G : informations de validation du fichier IGC
                    self.lignesG.append(ligne)
                elif ligne[0].upper() == "K" :  # lignes K : informations à des heures non régulières (wind direction (wdi), wind speed (wve), etc.)
                    if len(self.lignesJ)!=0:    #  on ignore les ligneK quand il n'existe pas de ligneJ
                        self.lignesK.append(LigneK(ligne,self.lignesJ[0]))
        self.fichierIgc.close()
        '''print "lignes A : ",len(self.lignesA)
        print "lignes H : ",len(self.lignesH)
        print "lignes I : ",len(self.lignesI)
        print "lignes J : ",len(self.lignesJ)
        print "lignes B : ",len(self.lignesB)
        print "lignes K : ",len(self.lignesK)
        print "lignes G : ",len(self.lignesG)'''
    def getTimeStamp (self,rangLigneB):
        ''' retourne le timestamp d'une ligneB (position) '''
        dateVol=self.date
        heureUTCLigneB=self.lignesB[rangLigneB].heureUTC
        jourPos= int(dateVol[0:2])
        moisPos= int(dateVol[2:4])
        anPos= int(dateVol[4:7])+2000
        heurePos= int(heureUTCLigneB[0:2])
        minutePos= int(heureUTCLigneB[2:4])
        secondePos= int(heureUTCLigneB[4:6])
        timestampPos = time.mktime((anPos,moisPos,jourPos,heurePos,minutePos,secondePos,0,0,-1)) # -1 indique que c'est une heure UTC
        return int(timestampPos)
    def getDateTime(self,timeStamp):
        return datetime.datetime.fromtimestamp(timeStamp)
    def getDeltaSecondes (self,rangLigneB):
        ''' retourne la durée écoulée depuis la position précédante '''
        if (rangLigneB==0): return None
        else : return self.getTimeStamp(rangLigneB)- self.getTimeStamp(rangLigneB-1)
    def getVz(self,rangLigneB):
        ''' retourne la vitesse verticale (m/s) par rapport à la position précédante '''
        dt=self.getDeltaSecondes(rangLigneB)
        if dt==None : return None
        elif dt==0 : return None
        else :
            alt=self.lignesB[rangLigneB].pressAlt
            altPrec=self.lignesB[rangLigneB-1].pressAlt
            vz= (alt-altPrec)/dt
            return vz
    def getDistance(self,rangLigneB):
        ''' retourne la distance (m) par rapport à la précédante position '''
        if (rangLigneB==0):
            return None
        else :
            return distanceOrthodromique(self.lignesB[rangLigneB-1].long,self.lignesB[rangLigneB-1].lat,self.lignesB[rangLigneB].long,self.lignesB[rangLigneB].lat)
    def getCapVitesse(self,rangLigneB):
        dt=self.getDeltaSecondes(rangLigneB)
        if dt==None or dt==0: return(None,None)
        lon=self.lignesB[rangLigneB].long
        lonPrec=self.lignesB[rangLigneB-1].long
        lat=self.lignesB[rangLigneB].lat
        latPrec=self.lignesB[rangLigneB-1].lat
        rep=capVitesse(lonPrec,latPrec,lon,lat,dt)
        return rep
class LigneI:
    ''' Description des informations complémetaires éventuelles dans les lignesB  '''
    def __init__(self,ligneI):
        self.isOK=False
        try:
            self.ligneI=ligneI
            self.codes=[]
            self.nbParam=int(ligneI[1:3])
            for i in range(self.nbParam):
                rang=3+i*7
                deb  =ligneI[rang+0:rang+2]
                fin  =ligneI[rang+2:rang+4]
                code =ligneI[rang+4:rang+7]
                self.codes.append((int(deb),int(fin),code))
            self.isOK=True
        except Exception,e:
            print "exception dans LigneI :",e  # alors la ligneI sera déclarée no OK
class LigneB:
    ''' une position (fix) décrite dans le fichier igc '''
    def __init__(self,ligneB,ligneI):
        self.isOK=False
        try:
            self.ligneB=ligneB
            self.ligneI=ligneI.ligneI
            self.heureUTC=ligneB[1:7]           # heure UTC
            self.intlat=ligneB[7:14]            # latiude  : ddmm,mmm
            deglat=float(self.intlat[0:2])
            minlat=float(self.intlat[2:7])/1000.
            self.lat= deglat+(minlat/60.)
            self.n_s=ligneB[14]                 # latitude nord ou sud
            if (self.n_s.upper()=="S"): self.lat=-self.lat   # les latitudes sud seront négatives
            self.intlong=ligneB[15:23]          # longitude : dddmm,mmm
            deglong=float(self.intlong[0:3])
            minlong=float(self.intlong[3:8])/1000.
            self.long= deglong+(minlong/60.)
            self.w_e=ligneB[23]                 # longitude ouest ou est
            if (self.w_e.upper()=="W"): self.long=-self.long   # les longitudes ouest seront seront négatives
            self.fixValidity=ligneB[24]         # A ou V
            self.intpressAlt=ligneB[25:30]      # altitude au dessus du 1015 mb : aaaaa(m)
            self.pressAlt=float(self.intpressAlt)
            self.intgpsAlt=ligneB[30:35]        # altitude au dessus du géoïde  : aaaaa(m)
            self.gpsAlt=float(self.intgpsAlt)
            if ligneI.nbParam != 0:             # décodage de la partie de la ligneB décrite par la ligneI
                for i in range(ligneI.nbParam):
                    (deb,fin,code)=ligneI.codes[i]
                    self.__dict__[code] = ligneB[deb-1:fin]
            self.isOK=True
        except Exception,e:
            print "exception dans LigneB :",e  # alors la ligneB sera déclarée no OK
    def affiche(self):
        #print "**************"
        #print self.ligneI
        #print self.ligneB
        print self.__dict__
class LigneK:
    ''' information à des heures non régulières '''
    def __init__(self,ligneK,ligneJ):
        self.ligneK=ligneK
        self.ligneJ=ligneJ.ligneJ
        self.heureUTC=ligneK[1:7]
        if ligneJ.nbParam != 0:
            for i in range(ligneJ.nbParam):
                (deb,fin,code)=ligneJ.codes[i]
                self.__dict__[code] = ligneK[deb-1:fin]
    def affiche(self):
        print self.__dict__
class LigneJ:
    ''' Descrition du contenu des lignesK apériodiques '''
    def __init__(self,ligneJ):
        self.ligneJ=ligneJ
        self.codes=[]
        self.nbParam=int(ligneJ[1:3])
        for i in range(self.nbParam):
            rang=3+i*7
            deb  =ligneJ[rang+0:rang+2]
            fin  =ligneJ[rang+2:rang+4]
            code =ligneJ[rang+4:rang+7]
            self.codes.append((int(deb),int(fin),code))
'''
path="20140627 Saint-Auban 27 juin 2014 Discus 2b DP Copie de 46RXI0H1.igc"
fich= FichierIGC(path)
dateVol=fich.date
for i in range(len(fich.lignesB)):
    heurePos=fich.lignesB[i].heureUTC
    print i,fich.getDateTime(fich.getTimeStamp(i)),fich.getDeltaSecondes(i),\
            fich.lignesB[i].lat,fich.lignesB[i].long,fich.getDistance(i),fich.getCapVitesse(i),fich.lignesB[i].pressAlt,fich.getVz(i)
'''
dropboxpath= "E:/Jean Pierre/Dropbox/"  # PC portable Lille
#dropboxpath= "J:/Dropbox/"              # PC fixe Paris
onedrivepath = "E:/Jean Pierre/OneDrive/"      # PC portable Lille
#onedrivepath = "J:/OneDrive/"  # PC fixe Paris

#basepath=onedrivepath+"Vol a voile\Positions.mdb"
basepath=onedrivepath+"Vol a voile/Positions.sqlite"
import sqlite3
conn = sqlite3.connect(basepath)      # ouverture de la base"

'''
import pypyodbc

repertBase=onedrivepath+"Vol a Voile/"
os.chdir(repertBase)
#pypyodbc.win_create_mdb("Positions.mdb")
conn = pypyodbc.win_connect_mdb("Positions.mdb")'''
cur=conn.cursor()
cur.execute("DROP TABLE Positions")
#cur.execute("CREATE TABLE Positions(idVol BLOB,date TEXT,heureUTC TEXT,latitude REAL,longitude REAL,altitude REAL)")
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

repertIGC=onedrivepath+"Vol a Voile/Fichier igc degribes/"
os.chdir(repertIGC)
nbfich=0
nblignesB=0
#for path in os.listdir(repertIGC):
for i in range(5000):
    path = os.listdir(repertIGC)[i]
    nbfich=nbfich+1
    print nbfich
    fich=FichierIGC(path)
    numeroVol=path
    print "nb de lignesB : ",len(fich.lignesB)
    if len(fich.lignesI)!=0:
        print "nb de lignesI : ",len(fich.lignesI)," contenu : " ,fich.lignesI[0].ligneI
    else:
        print "nb de lignesI : ",len(fich.lignesI)
    print "nb de lignesK : ",len(fich.lignesK)
    print "date : ",fich.date
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
print "nb fichiers traites :",nbfich
print "nb lignesB ajoutees :",nblignesB
print "nb moyen par fichier :", nblignesB/nbfich
