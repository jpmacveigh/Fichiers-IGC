# Créé par jpmv, le 21/10/2014
import pypyodbc
#pypyodbc.win_create_mdb("salesdb.mdb")
#conn = pypyodbc.connect("Driver = {Microsoft Access Driver (*. Mdb)}; DBQ = salesdb.mdb")
conn = pypyodbc.win_connect_mdb("salesdb.mdb")
cur=conn.cursor()
cur.execute("DROP TABLE saleout")
cur.execute("CREATE TABLE saleout ( ID COUNTER PRIMARY KEY, \
customer_name VARCHAR(25), \
product_name VARCHAR(30), \
price float, \
volume int, \
sell_time datetime);")
cur.commit()
name="totogf"
cur.execute("INSERT INTO saleout(customer_name,product_name,price,volume,sell_time) \
VALUES(?,?,?,?,?)",(name,'Lenovo P780',1250,2,'2012-1-21'))
cur.execute("INSERT INTO saleout(customer_name,product_name,price,volume,sell_time) \
VALUES(?,?,?,?,?)",(u'Yang Tianzhen','Apple IPhone 5',6000.1,1,'2012-1-21'))
cur.execute("INSERT INTO saleout(customer_name,product_name,price,volume,sell_time) \
VALUES(?,?,?,?,?)",(u'Zheng Xianshi','Huawei G700',5100.5,1,'2012-1-22'))
cur.execute("INSERT INTO saleout(customer_name,product_name,price,volume,sell_time) \
VALUES(?,?,?,?,?)",(u'Mo Xiaomin','Huawei G700',5200.5,1,'2012-1-22'))
cur.execute("INSERT INTO saleout(customer_name,product_name,price,volume,sell_time) \
VALUES(?,?,?,?,?)",(u'Gu Xiaobai','Lenovo P780',1250,1,'2012-1-22'))
cur.commit()
cur.execute("SELECT * FROM saleout")
for desc in cur.description:
    print desc[0]
for row in cur.fetchall():
    print row
cur.close()
conn.close()