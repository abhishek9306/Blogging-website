import sqlite3

con=sqlite3.connect("database.db")

print('hello')
con.execute('CREATE TABLE IF NOT EXISTS blog (id INTEGER PRIMARY KEY AUTOINCREMENT ,Title TEXT(150), Image TEXT(200), URLs TEXT(200),Panda TEXT(100), Content TEXT(2000))')

print('world')
con.close()

con = sqlite3.connect('database.db')
cur = con.cursor()
cur.execute('select * from blog')
r = cur.fetchall()
print(r)
con.commit()