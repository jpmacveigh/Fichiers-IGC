from FichierIGC import FichierIGC
from Terrains import Terrains
import json
#path ="20140627 Saint-Auban 27 juin 2014 Discus 2b DP Copie de 46RXI0H1.igc"
#path ="20190525 Bondues 25 mai 2019 Pegase DR.igc"
#path ="20190616-2 Bondues 16 juin 2019 Discus GI.igc"
#path="20190601 Soissons 1er juin 2019 Pégase DR.igc"
#path="20180717 Issoudun 17 juillet 2018 Janus AA.igc"
#path="20180718 Issoudun 18 juillet 2018 Janus AA.igc"
path="20150626 Saint-Auban 26 juin 2015 Ventus 2cx AC-2.igc"
#path="20200515 Bondues 15 mai 2020 Jean DN.igc"
#path="20200521 Bondues 21 mai 2020 Pégas EM.igc"
#path="NetCoupe2020_7555.igc"
#path="NetCoupe2020_9811_Mazalerat_11_juillet_2020.igc"
#path="NetCoupe2020_22.igc"
#path="NetCoupe2020_2658.igc"
#path="20210416 Bondues 16 avril 2021 Jean Astir DN.igc"
#path="NetCoupe2021_6898_Alexandre_Fierain_7_mai_2021.igc"
#path="20210529 Bondues 29 mai 2021 Discus GI.igc"
terrains=Terrains()
def analyseMaxiAltitude(path,write=True):
    """
    Recherche le jour, le terrain de décollage et l'altitude maximale atteinte par un vol
    """
    flight=FichierIGC(path)
    if flight.isOK:
        maximum=flight.getAltitudeMaxi()
        decollage=flight.positionTakeOff()
        nearest=terrains.nearestTerrain(decollage.long,decollage.lat)
        print(decollage.date,decollage.heureUTC,nearest[0],nearest[1][1],maximum[0].date,maximum[0].heureUTC,maximum[1])
        if write :
            file.write(json.dumps({
                "path":path.split("\\")[-1],
                "dec_date":decollage.date,
                "dec_heure":decollage.heureUTC,
                "nearest_dist":nearest[0],
                "nearest":nearest[1][1],
                "maxi_date":maximum[0].date,
                "maxi_heure":maximum[0].heureUTC,
                "maxi_longi":maximum[0].long,
                "maxi_lati":maximum[0].lat,
                "altiMax":maximum[1]
            })+"\n")

import os
file=open("maximums_new.txt","w") # fichier qui va recevoir les résultats
leDir=".\\NetCoupe"
lesPaths=os.listdir(leDir)
for path in lesPaths :
    name,ext=path.split(".")
    if (ext=="igc" and "new" in name):
        print(path)
        analyseMaxiAltitude(leDir+"\\"+path,True)
file.close()
