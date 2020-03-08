# Créé par jpmv, le 27/02/2015
path="positions.txt"
n=0
fichierPositions = open(path,"r")
for ligne in fichierPositions:
    ligne=ligne.replace("\n","")
    n=n+1
    if (n%1000==0): print (n,ligne)
print (n)
fichierPositions.close()
