import sqlite3

#connect to database
conn = sqlite3.connect('CUSTOMERS.db')

#create a cursor object
c = conn.cursor()

#update data in the table
c.execute("UPDATE CUSTOMERS SET wallet = 100 WHERE name = 'John Doe'")

#save changes
conn.commit()

#select data from table
c.execute("SELECT * FROM CUSTOMERS")

#fetch all records
records = c.fetchall()

#print records
for record in records:
	print(record)
	
#close connection
conn.close()
