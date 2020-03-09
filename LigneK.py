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
        print (self.__dict__)