import sqlite3
from sqlite3 import Error
import json
import re
from collections import OrderedDict

def num(s):
	s = re.sub(r"^.*?([0-9][0-9.]*).*$", r"\1", s)
	try:
		return int(s)
	except ValueError:
		return float(s)

def create_and_insert(cursor):
	datacoll = json.load(open('out.json'), object_pairs_hook=OrderedDict)
	tobeinserted = []
	for data in datacoll:
		app = list(list(data.values())[0].values())
		if len(app) == 17: 
			updout = []
			# print(app)
			for ind, upd in enumerate(app):
				if ind in [1, 2, 3, 4, 10, 13, 16]: 
					try:
						updout.append(num(upd))
					except:
						updout.append(-1)
				else : updout.append(upd)
			tobeinserted.append(updout)
	print(tobeinserted)

	for row in cursor.execute("CREATE TABLE IF NOT EXISTS specifications (dualsim int, frontcamera int, internal int, battery int, ram int, fingerprint int, maxbudget int, _3g int, model varchar(100), os varchar(100), display int, chipset varchar(100), brand varchar(20), rearcamera int, cpu varchar(100), _4g int, minbudget int);"):
		print(row)

	for row in cursor.executemany('INSERT INTO specifications VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', tobeinserted):
		print(row)


def create_connection(db_file):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
		return None

conn = create_connection("database.db")
if conn is None: exit(1)
c = conn.cursor()


c.execute("DROP TABLE specifications;")
create_and_insert(c)
	# print(row)

conn.commit()
conn.close()