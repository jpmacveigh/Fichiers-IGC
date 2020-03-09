from FichierIGC import FichierIGC
path ="20140627 Saint-Auban 27 juin 2014 Discus 2b DP Copie de 46RXI0H1.igc"
flight=FichierIGC(path)
#flight.affiche()
for i in range(250):
    print(i,flight.getDeltaSecondes(i),flight.getDistance(i),flight.lignesB[i].gpsAlt,flight.getCapVitesse(i),flight.deltaCap(i),flight.getVz(i))