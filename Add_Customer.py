import sqlite3

# connect to the database
conn = sqlite3.connect('CUSTOMERS.db')

# create a cursor object
c = conn.cursor()

# insert data into the table
c.execute("INSERT INTO CUSTOMERS (id, name, wallet) VALUES (2411, 'CHIRAG', 1000)")
#c.execute("INSERT INTO employees (id, name, wallet) VALUES (2, 'Jane Doe', 25)")

# save the changes
conn.commit()

# close the connection
conn.close()
