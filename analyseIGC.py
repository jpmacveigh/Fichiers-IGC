from FichierIGC import FichierIGC
path ="20140627 Saint-Auban 27 juin 2014 Discus 2b DP Copie de 46RXI0H1.igc"
flight=FichierIGC(path)
#flight.affiche()
for i in range(150):
    print(i,flight.getDateTime(i),flight.getDistance(i),flight.getCapVitesse(i),flight.getVz(i))