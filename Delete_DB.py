import sqlite3

# connect to the database
conn = sqlite3.connect('CUSTOMERS.db')

# create a cursor object
c = conn.cursor()

# delete data from the table
c.execute("DELETE FROM CUSTOMERS WHERE name = 'Jane Doe'")

# save the changes
conn.commit()

# select data from the table
c.execute("SELECT * FROM CUSTOMERS")

# fetch all the records
records = c.fetchall()

# print the records
for record in records:
    print(record)

# close the connection
conn.close()
