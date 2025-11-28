import sqlite3 as sql

#connecting to the database =>
con = sql.connect("Storage.db")
c = con.cursor()

#Creating the Database for users =>
c.execute(""" CREATE TABLE IF NOT EXISTS USERS(id integer primary key AUTOINCREMENT, username TEXT VARCHAR(20) UNIQUE,
    GymName TEXT VARCHAR(30), Email TEXT VARCHAR(20) UNIQUE, City TEXT VARCHAR(20), Password TEXT) """)
