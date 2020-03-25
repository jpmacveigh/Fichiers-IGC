# Créé par AD, le 15/11/2014
import datetime
import time
def getDateTime(timeStamp):
        ''' retourne date '''
        return datetime.datetime.fromtimestamp(timeStamp)
def getTimeStamp (an,mois,jour,heure,minute,seconde):
        ''' retourne le timestamp  '''
        timestampPos = time.mktime((an,mois,jour,heure,minute,seconde,0,0,-1)) # -1 indique que c'est une heure UTC
        return int(timestampPos)


print("Il est en moment (heure locale) :", datetime.datetime.today().isoformat(), " time_stamp: ", time.time())
print("Il est en moment (heure UTC)    :", datetime.datetime.utcnow().isoformat(), " time_stamp: ", time.time())


