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