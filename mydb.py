import mysql.connector

#connect to database

database= mysql.connector.connect(    
    host = 'localhost',
    user = 'root',
    password = 'Yagnik9@',

)

# prepare a cursor object
cursorobject = database.cursor()

#create a database
cursorobject.execute("CREATE DATABASE crm")

print("All Done!")
