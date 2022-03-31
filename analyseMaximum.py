from FichierIGC import FichierIGC
#path ="20140627 Saint-Auban 27 juin 2014 Discus 2b DP Copie de 46RXI0H1.igc"
#path ="20190525 Bondues 25 mai 2019 Pegase DR.igc"
#path ="20190616-2 Bondues 16 juin 2019 Discus GI.igc"
#path="20190601 Soissons 1er juin 2019 Pégase DR.igc"
#path="20180717 Issoudun 17 juillet 2018 Janus AA.igc"
#path="20180718 Issoudun 18 juillet 2018 Janus AA.igc"
#path="20150626 Saint-Auban 26 juin 2015 Ventus 2cx AC-2.igc"
#path="20200515 Bondues 15 mai 2020 Jean DN.igc"
#path="20200521 Bondues 21 mai 2020 Pégas EM.igc"
#path="NetCoupe2020_7555.igc"
#path="NetCoupe2020_9811_Mazalerat_11_juillet_2020.igc"
#path="NetCoupe2020_22.igc"
#path="NetCoupe2020_2658.igc"
#path="20210416 Bondues 16 avril 2021 Jean Astir DN.igc"
#path="NetCoupe2021_6898_Alexandre_Fierain_7_mai_2021.igc"
path="20210529 Bondues 29 mai 2021 Discus GI.igc"
print(path)
flight=FichierIGC(path)
print(flight.getAltitudeMaxi())
flight.getAltitudeMaxi()[0].affiche()
print(flight.positionTakeOff())
flight.positionTakeOff().affiche()