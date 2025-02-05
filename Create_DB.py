import sqlite3

# connect to the database
conn = sqlite3.connect('CUSTOMERS.db')

# create a cursor object
c = conn.cursor()

# create a table
c.execute('''CREATE TABLE CUSTOMERS
             (id INT PRIMARY KEY NOT NULL,
              name TEXT NOT NULL,
              wallet INT NOT NULL)''')

# save the changes
conn.commit()

# close the connection
conn.close()
