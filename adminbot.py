''' Admin Bot for CloudBot project '''

import sqlite3 as sq
import sys
import os.path

''' The basic idea is to use the terminal window to
	quickly and easily add answers to cloudbot's
	database of answers. (answers.db)           '''
	
#Query the database
if os.path.isfile("answers.db"):
	conn = sq.connect("answers.db")
	c = conn.cursor()
else:
	print("Error: No matching database")
	sys.exit(1)
answers = c.execute("SELECT * FROM unknowns WHERE has_answer=0")
for row in answers:
	print("Question: " + row[1])
	answer = input("Answer: ")
	c.execute("UPDATE unknowns set admin_answer=? WHERE question=?",(answer,row[1]))
	c.execute("UPDATE unknowns set has_answer=1 WHERE question=?",row[1])
	conn.commit()
	print(".......................................")
	
conn.close()
	
	
