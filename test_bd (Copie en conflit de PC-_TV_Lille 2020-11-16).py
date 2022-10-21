# Créé par jpmv, le 14/10/2014
'''
import dbi
import odbc
from pprint import pprint
connex = odbc.odbc("essai.mdb")
curseur = connex.cursor()
curseur.execute("SELECT temp,hum FROM data")
data = curseur.fetchall()
pprint (data)
curseur.close()
connex.close()'''

'''import pyodbc

DBfile = "essai.mdb"
conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb)};DBQ='+DBfile)
cursor = conn.cursor()

SQL = 'SELECT temp,hum FROM data;'

cursor.close()
conn.close()'''

# essai sqlite
import sqlite3
conn = sqlite3.connect("essai.sqlite")      # ouverture de la base"
#conn.row_factory = sqlite3.Row              # accès facile aux colonnes
cursor = conn.cursor()                      # obtention d'un curseur
cursor.execute("SELECT temp,hum FROM vols")
all_rows = cursor.fetchall()
for row in all_rows:
    print row
'''for ligne in cursor:
    print ligne'''
cursor.close()



