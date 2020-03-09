# Créé par AD, le 02/11/2014
# essai anydbm
import anydbm
'''dbmfile = anydbm.open('blabla', 'c')
dbmfile['foo'] = 'perrier c foo'
dbmfile['bar'] = 'cd bar ; more beer'
print dbmfile['foo']
print dbmfile['bar']
dbmfile.close()
'''
db=anydbm.open("test_anydbm","c")
for i in range(10):
    db["numero"]=str(i)
db.close()
db = anydbm.open("test_anydbm","r")
try:
    print 'keys():', db.keys()
    for k, v in db.iteritems():
        print 'iterating:', k, v

finally:
    db.close()