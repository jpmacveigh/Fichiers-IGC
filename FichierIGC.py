# -*- coding: utf-8 -*-
from LigneI import LigneI
from LigneB import LigneB
from LigneK import LigneK
from LigneJ import LigneJ
import time
import datetime
from distanceOrthodromique import distanceOrthodromique
from capVitesse import capVitesse
from deltaCap import deltaCap
class FichierIGC:
    def __init__(self,path):   # constructeur à partir du path du ficier IGC
        print ("nom du fichier igc : ",path)
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
                    if ligneB.isOK : self.lignesB.append(ligneB)   # on ignore les lignesB mal formées
                elif ligne[0].upper() == "G" :  # lignes G : informations de validation du fichier IGC
                    self.lignesG.append(ligne)
                elif ligne[0].upper() == "K" :  # lignes K : informations à des heures non régulières (wind direction (wdi), wind speed (wve), etc.)
                    if len(self.lignesJ)!=0:    #  on ignore les ligneK quand il n'existe pas de ligneJ
                        self.lignesK.append(LigneK(ligne,self.lignesJ[0]))
        self.fichierIgc.close()   # fermeture du fichier IGC
    
    def getDateTime(self,rangLigneB):
        ''' retourne la date et heure UTC d'une position '''
        return datetime.datetime.fromtimestamp(self.getTimeStamp(rangLigneB))
    
    def getTimeStamp (self,rangLigneB):
        ''' retourne le timestamp d'une position '''
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
            alt=self.lignesB[rangLigneB].pressAlt
            altPrec=self.lignesB[rangLigneB-1].pressAlt
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