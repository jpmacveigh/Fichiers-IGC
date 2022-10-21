import os as os
chemin="."
arbre=os.walk(chemin)
for rep in arbre:
    print(rep)