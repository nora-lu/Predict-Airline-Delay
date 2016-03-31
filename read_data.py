# Install sqlalchemy and pymysql
# Panda uses sqlalchemy engine to work with the database, directly convert the query result into a DataFrame

from sqlalchemy import create_engine
from pandas import DataFrame
from pprint import pprint

server = 'cs586.cpzwisqfd2pn.us-west-2.rds.amazonaws.com:3306'
db = 'cs586'
username = 'your_username'
pwd = 'your_pwd'
engine_str = 'mysql+pymysql://{}:{}@{}/{}'.format(username, pwd, server, db)

if __name__ == "__main__":
    engine = create_engine(engine_str)
    connection = engine.connect()
    query_res = connection.execute("SELECT * FROM table2010 LIMIT 1, 1000")

    df = DataFrame(query_res.fetchall())
    df.columns = query_res.keys()

    pprint(df)

    connection.close()
    engine.dispose()









# # https://github.com/PyMySQL/PyMySQL
# import pymysql.cursors

# # Connect to the database
# connection = pymysql.connect(host='cs586.cpzwisqfd2pn.us-west-2.rds.amazonaws.com',
#                             port=3306,
#                             user='your_username',
#                             password='your_password',
#                             db='cs586')

# try:
#     with connection.cursor() as cur:
#         cur.execute("SELECT * FROM cs586.table2010 LIMIT 1, 1000")
#         for row in cur:
#             print(row)
# finally:
#     connection.close()



# #MySQLdb is installed as http://www.tutorialspoint.com/python/python_database_access.htm
# #conda command may also work but not tested heres
# import MySQLdb

# config = {'host':"cs586.cpzwisqfd2pn.us-west-2.rds.amazonaws.com",
#           'user':"your_username",
#           'passwd':"your_password"}

# db = MySQLdb.connect(**config)

# cur = db.cursor()

# cur.execute("USE cs586")

# cur.execute("SELECT * FROM table2010 LIMIT 100")

# for row in cur.fetchall():
#     print row

# db.close()
