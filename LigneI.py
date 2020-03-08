# -*- coding: utf8 -*-
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
        except (Exception,e):
            print ("exception dans LigneI :",e)  # alors la ligneI sera déclarée no OK