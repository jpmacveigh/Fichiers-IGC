# -*- coding: utf8 -*-
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
        except (Exception,e):
            print ("exception dans LigneB :",e)  # alors la ligneB sera déclarée no OK
    def affiche(self):
        #print "**************"
        #print self.ligneI
        #print self.ligneB
        print (self.__dict__)