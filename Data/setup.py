import os.path
from dotenv import load_dotenv

import sqlite3 as sql
import bcrypt

#Loading the first User information from .env file =>
load_dotenv()
firstname = os.getenv("firstname")
lastname = os.getenv("lastname")
username = os.getenv("username")
gymname = os.getenv("gymname")
email = os.getenv("email")
city = os.getenv("city")
password = os.getenv("password")

#bcrypt the password =>
bytes = password.encode('utf-8') 
salt = bcrypt.gensalt() 
hash = bcrypt.hashpw(bytes, salt)

#connecting to the database =>
con = sql.connect("Storage.db")
c = con.cursor()

#Creating the Database for users =>
c.execute(""" CREATE TABLE IF NOT EXISTS USERS(id integer primary key AUTOINCREMENT, username TEXT VARCHAR(20) UNIQUE,
      LastName TEXT VARCHAR(30), FirstName TEXT VARCHAR(30),
      GymName TEXT VARCHAR(30), Email TEXT VARCHAR(20) UNIQUE, City TEXT VARCHAR(20), Password TEXT) """)

#Inserting the First user information into the database =>
c.execute(""" INSERT INTO USERS(username, FirstName, LastName, GymName, Email, City, Password) VALUES("{}", "{}", "{}", "{}", "{}", "{}", "{}"); """.format(username, firstname, lastname, gymname, email, city, hash))
con.commit()
