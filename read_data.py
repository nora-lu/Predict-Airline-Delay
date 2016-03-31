# https://github.com/PyMySQL/PyMySQL
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='cs586.cpzwisqfd2pn.us-west-2.rds.amazonaws.com',
                             port=3306,
                             user='your_username',
                             password='your_password',
                             db='cs586')

try:
    with connection.cursor() as cur:
        cur.execute("SELECT * FROM cs586.table2010 LIMIT 1, 1000")
        for row in cur:
            print(row)
finally:
    connection.close()



#MySQLdb is installed as http://www.tutorialspoint.com/python/python_database_access.htm
#conda command may also work but not tested heres
import MySQLdb

config = {'host':"cs586.cpzwisqfd2pn.us-west-2.rds.amazonaws.com",
          'user':"your_username",
          'passwd':"your_password"}

db = MySQLdb.connect(**config)

cur = db.cursor()

cur.execute("USE cs586")

cur.execute("SELECT * FROM table2010 LIMIT 100")

for row in cur.fetchall():
    print row

db.close()
