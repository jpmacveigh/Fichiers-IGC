# Créé par jpmv, le 30/10/2014
import pypyodbc
import os
def constructSelectWhereWhen(latMin,latMax,longMin,longMax,tstampMin,tstampMax):
    ch =""
    ch=ch+"SELECT Min(Vz) AS MinVz, Avg(Vz) AS MoyenneDeVz, Max(Vz) AS MaxVz, Count(Vz) AS CompteDeVz , "
    ch=ch+"%f"%latMin+" AS LatMin, "+"%f"%latMax+" AS LatMax , "
    ch=ch+"%f"%longMin+" AS LongMin, "+"%f"%longMax+" AS LongMax, "
    ch=ch+str(tstampMin)+" AS TsMin, "+str(tstampMax)+" AS TsMax "
    ch=ch+" FROM Positions WHERE "
    ch=ch+"((latitude  BETWEEN "+str(latMin) +" AND "+str(latMax)+") AND "
    ch=ch+ "(longitude BETWEEN "+str(longMin)+" AND "+str(longMax)+") AND "
    ch=ch+ "(t_stamp   BETWEEN "+str(tstampMin)+" AND "+str(tstampMax)+"));"
    #print ch
    return ch
#onedrivepath = "E:/Jean Pierre/OneDrive/"      # PC portable Lille
onedrivepath = "J:/OneDrive/"  # PC fixe Paris
#basepath=onedrivepath+"Vol a voile\Positions.mdb"
repertBase=onedrivepath+"Vol a Voile/"
os.chdir(repertBase)
conn = pypyodbc.win_connect_mdb("Positions.mdb")
#import sqlite3
#conn = sqlite3.connect("Positions.sqlite")
cur=conn.cursor()
'''
cur.execute("SELECT Min(Vz) AS MinVz,Avg(Vz) AS MoyenneDeVz,Max(Vz) AS MaxVz, Count(Vz) AS CompteDeVz \
            FROM Positions \
            WHERE (((latitude)>43.1 And (latitude)<43.2) \
               AND ((longitude)>0.35 And (longitude)<0.4) \
               AND ((t_stamp)>1295953682 And(t_stamp)<1306595040));")
cur.execute("SELECT Avg(Vz) AS MoyenneDeVz, Count(Vz) AS CompteDeVz \
            FROM Positions \
            WHERE ((latitude BETWEEN 43.1 AND 43.2 ) \
               AND (longitude BETWEEN 0.35 AND 0.40) \
               AND (t_stamp BETWEEN 1295953682 AND 1306595040));")
for row in cur.fetchall():
    print row
'''
for i in range(10):
    latMin=43.9+i*0.01
    latMax=latMin+0.01
    cur.execute(constructSelectWhereWhen(latMin,latMax,6.35,6.45,1306879210,1312149599))
    #print cur.description
    for row in cur.fetchall():
        print (row)
cur.close()
conn.close()

