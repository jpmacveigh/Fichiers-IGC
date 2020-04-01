from FichierIGC import FichierIGC
#path ="20140627 Saint-Auban 27 juin 2014 Discus 2b DP Copie de 46RXI0H1.igc"
#path ="20190525 Bondues 25 mai 2019 Pégase DR.igc"
path ="20190616-2 Bondues 16 juin 2019 Discus GI.igc"
#path="NetCoupe2020_22.igc"
#path="NetCoupe2020_2658.igc"
flight=FichierIGC(path)
lesLifts=flight.make_les_lifts()
print (len(lesLifts))
i=1
for lift in lesLifts :
    print ("asendance n°: ",i)
    lift.affiche()
    i=i+1

#flight.look_for_lift()
flight.make_SQLITE3_file()
flight.make_histogramme_des_vitesses()
#for i in range(5):
 #   flight.lignesB[i].affiche()
"""
#flight.affiche()
for i in range(len(flight.lignesB)):
    #print(i,flight.getDeltaSecondes(i),flight.getDistance(i),flight.lignesB[i].gpsAlt,flight.getCapVitesse(i),flight.deltaCap(i),flight.getVz(i))
    if (flight.deltaCap(i) and abs(flight.deltaCap(i))>=50.) : print(i,flight.getDeltaSecondes(i),flight.getDistance(i),flight.lignesB[i].gpsAlt,flight.getCapVitesse(i),flight.deltaCap(i),flight.getVz(i))
"""