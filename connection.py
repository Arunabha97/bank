__author__ = 'user'

import cx_Oracle
# you must have Oracle database userId and password for connection from database.
con = cx_Oracle.connect("SYSTEM/1234@localhost/xe")
cur = con.cursor()
