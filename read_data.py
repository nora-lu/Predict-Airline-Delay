import MySQLdb

config = {'host':"cs586.cpzwisqfd2pn.us-west-2.rds.amazonaws.com",
          'user':"luqian",
          'passwd':"your_password"}

db = MySQLdb.connect(**config)

cur = db.cursor()

cur.execute("USE cs586")

cur.execute("SELECT * FROM table2010 LIMIT 100")

for row in cur.fetchall():
    print row

db.close()
