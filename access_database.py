import sqlite3
con = sqlite3.connect('db.sqlite3')
print("Database connected!")
print("Please input your SQL statement:")
sql = input()
cur = con.execute(sql)
print(cur.fetchall())
