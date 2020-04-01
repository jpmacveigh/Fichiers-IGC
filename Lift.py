class Lift :
    ''' Un ascendance définie par la listes des positions qui la compose '''
    def __init__(self,lift):
        self.lift=lift
        self.ts_deb=lift[0].getTimeStamp()
        self.ts_fin=lift[-1].getTimeStamp()
        self.datetime_deb=lift[0].getDateTime()
        self.datetime_fin=lift[-1].getDateTime()
        self.duree=self.ts_fin-self.ts_deb
        self.lati_deb=lift[0].lat
        self.longi_deb=lift[0].long
        self.lati_fin=lift[-1].lat
        self.longi_fin=lift[-1].long
        self.alti_deb=lift[0].gpsAlt
        self.alti_fin=lift[-1].gpsAlt
        self.gain_alti=self.alti_fin-self.alti_deb
        assert self.duree > 0 , self.duree
        self.vz_moyenne=self.gain_alti/self.duree
        alti_min=10000
        alti_max= -100000
        for pos in self.lift:
            if pos.gpsAlt > alti_max : alti_max=pos.gpsAlt
            if pos.gpsAlt < alti_min : alti_min=pos.gpsAlt
        self.alti_min=alti_min
        self.alti_max=alti_max
    def affiche(self):
        print ("nombre de positions: ", len(self.lift))
        print ("debut à: ",self.ts_deb,"  fin à: ",self.ts_fin,"  durée(s) : ",self.duree)
        print ("début à: ",self.datetime_deb,"  fin à: ",self.datetime_fin)
        print ("alt debut: ",self.alti_deb,"  alt fin: ",self.alti_fin)
        print ("gain altitude: ",self.gain_alti,"  Vz moyenne: ",round(self.vz_moyenne,1))
        print ("alt mini: ",self.alti_min,"  alt maxi: ",self.alti_max)
        print ("*******************")
