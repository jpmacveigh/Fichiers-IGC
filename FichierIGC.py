from LigneI import LigneI
from LigneB import LigneB
from LigneK import LigneK
from LigneJ import LigneJ
from lowner_john_ellipse import *
from matplotlib import pyplot as plt
import time
import datetime
import os
import traceback
import sqlite3
import boto3
from distanceOrthodromique import distanceOrthodromique
from capVitesse import capVitesse
from deltaCap import deltaCap
from Lift import Lift
from trace_histogramme import trace_histogramme
class FichierIGC:    # Un fichier IGC tel qu'il est fourni par un Oudie2 (par exemple)
    def __init__(self,path):   # constructeur à partir du path du ficier IGC
        #print ("nom du fichier igc : ",path)
        self.isOK=False
        try:
            self.path=path
            self.fichierIgc = open(path,"r")   # ouverture du fichier IGC en lecture seule
            self.lignesB=[]
            self.lignesA=[]
            self.lignesH=[]
            self.lignesI=[]
            self.lignesJ=[]
            self.lignesG=[]
            self.lignesK=[]
            self.date="ddmmyy"
            heure_prec_ligneB="000000"
            for ligne in self.fichierIgc:           # itération sur toutes les lignes du ficheir IGC et on en teste le premier caractère
                ligne=ligne.replace("\n","")        # supression du caractère de fin de ligne
                if len(ligne) >0:                   # on ne traite pas les lignes vides, car j'en ai trouvées !
                    if ligne[0].upper() == "A" :    # ligne A : première ligne obligatoire
                        self.lignesA.append(ligne)
                    elif ligne[0].upper() == "H" : # lignes H : en-tête
                        self.lignesH.append(ligne)
                        if   ligne[1:10].upper()=="FDTEDATE:":  # nouvelle norme IGC après 2015
                            self.date=ligne[10:16]      # date du vol : ddmmyy
                        elif ligne[1:5].upper()=="FDTE":  # recherche de la date du vol
                            self.date=ligne[5:11]       # date du vol : ddmmyy
                    elif ligne[0].upper() == "I" :  # ligne I : (optionnelle) Précise les compléments des lignesB (vitessse sol(gsp), true track(trt), etc.)
                        ligneI=LigneI(ligne)
                        if ligneI.isOK : self.lignesI.append(ligneI) # on ignore les ligneI mal formées
                    elif ligne[0].upper() == "J" :  # ligne J : (optionnelle) Précise le contenu des lignesK
                        self.lignesJ.append(LigneJ(ligne))
                    elif ligne[0].upper() == "B" :  # lignes B : les positions GPS (fix) à des heures régulièrement espacées
                        ligneB=None
                        if len(self.lignesI)!=0:
                            ligneB=LigneB(ligne,self.lignesI[0],self.date)
                        else:
                            ligneB=LigneB(ligne,LigneI("I000000000"),self.date)  # cas où il n'y a pas de ligneI
                        if ligneB.isOK and (not ligneB.heureUTC==heure_prec_ligneB) :  # on ignore les lignesB mal formées et deux consécutives qui portent la même heure   
                            self.lignesB.append(ligneB)   
                            heure_prec_ligneB=ligneB.heureUTC               
                    elif ligne[0].upper() == "G" :  # lignes G : informations de validation du fichier IGC
                        self.lignesG.append(ligne)
                    elif ligne[0].upper() == "K" :  # lignes K : informations à des heures non régulières (wind direction (wdi), wind speed (wve), etc.)
                        if len(self.lignesJ)!=0:    #  on ignore les ligneK quand il n'existe pas de ligneJ
                            self.lignesK.append(LigneK(ligne,self.lignesJ[0]))
            for i in range(1,len(self.lignesB)) :  # on flague comme "inFlight" les LignesB pour lesquelles la vitesse est supérieure à un seuil
                #print(i,self.getCapVitesse(i)[1],self.lignesB[i-1].affiche(),self.lignesB[i].affiche())
                if (self.getCapVitesse(i)[1]>=25.):
                    self.lignesB[i].isInFlight=True
                    self.lignesB[i].cap_vitesse=self.getCapVitesse(i)
            self.lesInFlights=[ligne for ligne in self.lignesB if ligne.isInFlight==True]
            self.altiDecollage=self.positionTakeOff().gpsAlt
            poids_planeur=400. # poids du planeur en kg
            for ligne in self.lesInFlights:
                ligne.energie_potentielle=poids_planeur*9.81*(ligne.gpsAlt-self.altiDecollage) # l'énergie potentielle du planeur à cette position
                vms=ligne.cap_vitesse[1]/3.6 # vitesse du planeur en m/s
                ligne.energie_cinétique=0.5*poids_planeur*vms*vms # l'énergie cinétique du planeur à cette position
                #print(ligne.energie_potentielle,ligne.cap_vitesse[1],ligne.energie_cinétique)
            self.isOK=True
        except Exception as e :
            #print ("exception dans FichierIGC: ",e)  # alors le fichier IGC sera déclaré no OK
            self.isOK=False
            print ("Fichier IGC incorrect :",self.path)
            traceback.print_exc() 
        self.fichierIgc.close()   # fermeture du fichier IGC
    
    def make_SQLITE3_file (self):
        ''' Fabrique une BD Sqlite3 avec toutes les information relatives au fichiers IGC '''
        (file_name,_)=os.path.splitext(self.path)
        self.path_sqlite3=file_name+".sqlite"  # la BD aura le même nom que le fichier igc avec l'extension sqlite
        print (self.path_sqlite3)
        conn=sqlite3.connect(self.path_sqlite3)      # creation de la base Sqlite3"
        # création d'une tables pour les positions contenues dans la fichier IGC
        conn.execute("DROP TABLE IF EXISTS positions")    # effacement puis re-céation de la table positions
        conn.commit()
        cmd="CREATE TABLE positions("
        cmd=cmd+"id_posi INTEGER PRIMARY KEY AUTOINCREMENT,date TEXT,ts INTEGER,lati REAL,longi REAL,alti REAL,vz REAL, cap REAL,vit REAL,isLift TEXT)"
        conn.execute(cmd)
        conn.commit()
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
        # création d'une table pour les acsendances identifiées dans le ficheir IGC
        conn.execute("DROP TABLE IF EXISTS ascendances")    # effacement puis re-céation de la table positions
        conn.commit()
        cmd="CREATE TABLE ascendances("  # la table des ascendances
        cmd=cmd+"id_ascend INTEGER PRIMARY KEY AUTOINCREMENT,"
        cmd=cmd+"ts_deb INTEGER,ts_fin INTEGER,date_deb TEXT,date_fin TEXT,"
        cmd=cmd+"lati_deb REAL,longi_deb REAL,lati_fin REAL,longi_fin REAL,"
        cmd=cmd+"alti_deb INTEGER,alti_fin INTEGER,alti_min INETEGR,alti_max INTEGER,"
        cmd=cmd+"duree INTEGER,gain_alti INTEGER,vz_moy REAL,"
        cmd=cmd+"lati_centre REAL,longi_centre REAL, major_axis REAL, minor_axis REAL, rotation_angle REAL)"
        conn.execute(cmd)
        conn.commit()
        # Ecriture dans la table des ascendances
        list_champs= ["ts_deb","ts_fin","date_deb","date_fin"]
        list_champs=list_champs+["lati_deb","longi_deb","lati_fin","longi_fin"]
        list_champs=list_champs+["alti_deb","alti_fin","alti_min","alti_max"]
        list_champs=list_champs+["duree","gain_alti","vz_moy"]
        for asc in self.lesLifts :
            list_valeurs=[asc.ts_deb,asc.ts_fin,'"'+str(asc.datetime_deb) +'"','"'+str(asc.datetime_fin) +'"']
            list_valeurs=list_valeurs+[asc.lati_deb,asc.longi_deb,asc.lati_fin,asc.longi_fin]
            list_valeurs=list_valeurs+[asc.alti_deb,asc.alti_fin,asc.alti_min,asc.alti_max]
            list_valeurs=list_valeurs+[asc.duree,asc.gain_alti,asc.vz_moyenne]
            cmd=self.commande_insert("ascendances",list_champs,list_valeurs)
            conn.execute(cmd)
        conn.commit()
        conn.close()
        
    def send_les_fichiers_to_s3(self):
            # stockage du fichier sqlite créé dans un bucket de AWS S3
            bucket_name="volavoile"
            s3 = boto3.resource('s3')
            #s3.Object(bucket_name,'newfile.txt').put(Body=content)
            s3.Object(bucket_name,'igc_tempo.sqlite').put(Body=open(self.path_sqlite3,'rb'))
            s3.Object(bucket_name,self.path_sqlite3).put(Body=open(self.path_sqlite3,'rb'))
            s3.Object(bucket_name,self.path).put(Body=open(self.path,'rb'))
    def commande_insert(self,table_name,liste_champs,liste_valeurs):
        """
        Squelette d'une commande SQL INSERT
        """
        cmd='INSERT INTO '+table_name+' ('
        for champ in liste_champs:
            cmd=cmd+champ+','
        cmd=cmd[:-1]+') VALUES ('
        for valeur in liste_valeurs:
            cmd=cmd+str(valeur)+','
        cmd=cmd[:-1]+')'
        return (cmd)

    def make_les_ellipses(self):
        """
        On entoure tous les points de chaque chaque ascendance dans une elipse
        """
        conn=sqlite3.connect(self.path_sqlite3)
        res=conn.execute("SELECT ts_deb,ts_fin FROM ascendances").fetchall()  # lecture des ts de debut et fin des acendances
        conn.commit()
        num_asc=0
        for asc in self.lesLifts  :      # itérations sur les ascendances identifiées dans le fichier IGC
            cmd="SELECT longi,lati FROM positions WHERE ts>="
            cmd=cmd+str(res[num_asc][0])+" AND ts<="+str(res[num_asc][1])
            print (cmd)
            les_points= conn.execute(cmd).fetchall()   # lecture de la liste des positions de l'ascendance
            points=np.zeros((len(les_points),2))
            i=0
            for x in les_points:   #  fabrication du tableau d'entrée pour le programme de calcul de l'ellipse minimale
                #print(x)
                points[i,0]=x[0]
                points[i,1]=x[1]
                i=i+1
            #plt.figure()
            #plt.plot(points[:, 0], points[:, 1], '.')
            enclosing_ellipse = welzl(points)  # find enclosing Lowner-John ellipse           
            (centre,major_axis,minor_axis,rotation_angle)=enclosing_ellipse
            print(enclosing_ellipse)
            rotation_angle=rotation_angle
            cmd="UPDATE ascendances SET "
            cmd=cmd+"longi_centre = "+str(centre[0])+", "
            cmd=cmd+"lati_centre = "+str(centre[1])+", "
            cmd=cmd+"major_axis = "+str(major_axis)+", "
            cmd=cmd+"minor_axis = "+str(minor_axis)+", "
            cmd=cmd+"rotation_angle = "+str(rotation_angle)+" "
            cmd=cmd+" WHERE id_ascend = "+str(num_asc+1)
            print(cmd)
            conn.execute(cmd)    # écriture des paramètres de l'ellipse dans la table des ascendances
            conn.commit()
            #plot_ellipse(enclosing_ellipse, str='k--')  # plot resulting ellipse
            #plt.show()
            num_asc=num_asc+1
        self.send_les_fichiers_to_s3()    
    def getDateTime(self,rangLigneB):
        ''' retourne la date et heure UTC d'une position '''
        return datetime.datetime.utcfromtimestamp(self.getTimeStamp(rangLigneB))
    
    def getTimeStamp (self,rangLigneB):
        ''' retourne le timestamp d'une position '''
        return int(self.lignesB[rangLigneB].timestamp)

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
        if dt==None : return(None,None)
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
        ''' Détermine les positions en vol qui sont dans une ascendance '''
        res=[]
        deltat_lim=30         # durée de la fenêtre temporelle (s)
        seuil_z=30            # seuil d'élévation minimale sur la fenêtre teporelle (m)
        #distance_test=1500  # distance minimale (m)
        lesLignes=[]    # les positions qui sont dans la fenêtre temporelle
        lesInFlights=[ligne for ligne in self.lignesB if ligne.isInFlight==True] 
        lesLignes.append(lesInFlights[0])
        for ligne in lesInFlights:     # itération sur toutes les positions en vol du fichiers
            lesLignes.append(ligne)
            deltat= ligne.getTimeStamp()-lesLignes[0].getTimeStamp() 
            if (deltat)>=deltat_lim : # si on est à la fin de la fenêtre temporelle
                #distance=distanceOrthodromique(lesLignes[0].long,lesLignes[0].lat,ligne.long,ligne.lat) # distance parcourrue depuis l'entrée dans la fenêtre temporelle
                #if distance <= distance_test : # on est dans une ascendance
                deltaz=ligne.gpsAlt-lesLignes[0].gpsAlt  # différence d'altitude depuis l'entrée dans la fenêtre temporelle
                #print (lesLignes[0].getDateTime(),lesLignes[-1].getDateTime(),ligne.getDateTime())
                if deltaz>seuil_z :   # on est dans une ascendance
                    ligne.isLift=True
                    res.append(ligne)
                    #ligne.affiche(["lat","long"])
                while ligne.getTimeStamp()-lesLignes[0].getTimeStamp() > deltat_lim :
                    lesLignes.pop(0)  # on décalle la fenêtre d'une ligne en enlevant le premier point de la fenêtre
        print (len(res))
        return (res)

    def make_les_lifts(self):  # renvoi la listes des asendances du ficheir IGC
        ''' Renvoi la liste des asendances du ficheir IGC '''
        res=[]
        self.look_for_lift() # Recherche des positions qui sont dans une ascendance
        lesLifts=[]
        lift=[]  # une acsendance vide
        for ligne in self.lignesB:  # itération sur toutes les positions
            if not(ligne.isLift) :   # si la position est n'est pas dans une ascendance
                if len(lift) >0 : 
                    lesLifts.append(lift)
                    lift=[]
            else :                   # la posiiotn est dans une ascendance
                lift.append(ligne)
        if len(lift)>0 : lesLifts.append(lift)  # on ajoute l'escendance à la listes des ascendances
        for lift in lesLifts :
            if len(lift)>1 :
                asc=Lift(lift)   # on fabrique un objet "Lift"
                if (asc.duree>=60) : # on ne retient que les ascendances de plus de 60 secondes
                    res.append(asc)  # que l'on ajoute à la listes des ascendances
        self.lesLifts=res
        return (res)

    def make_histogramme_des_vitesses(self):
        """
        Trace l'histogramme des vitesses de toutes les LignesB
        """
        data=[]
        for i in range(1,len(self.lignesB)):
            data.append(self.getCapVitesse(i)[1])
        trace_histogramme(data,self.path,"Vitesses (Km/h)",100,-20.,200.)
    
    def getAltitudeMaxi(self):
        """
        Renvoi la position la plus elevée du fichier
        """
        max=-5000.
        for ligneB in self.lignesB:
            alti=ligneB.gpsAlt
            if alti>max :
                max=alti
                ligneBMax=ligneB
        return (ligneBMax,max)
    
    def positionTakeOff(self):
        """
        Renvoi la position du décollage
        """
        return (self.lesInFlights[0])

    
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