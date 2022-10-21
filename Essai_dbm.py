import dbm
import datetime
with dbm.open("test_dbm.dbm","n") as db:
    for i in range(5):
        #db[str(i)]=str(i)
        db[str(i)]=datetime.datetime.utcnow().isoformat()
with dbm.open("test_dbm.dbm","r") as db:
    print ('keys():', db.keys())
    for k in db.keys():
        print ('key:', k,'values',db[k])
