# Créé par jpmv, le 27/02/2015
path="J:/AsusSyncFolder/positions.txt"
n=0
fichierPositions = open(path,"r")
for ligne in fichierPositions:
    ligne=ligne.replace("\n","")
    n=n+1
    if (n%1000000==0): print (n)
print (n)
fichierPositions.close()
