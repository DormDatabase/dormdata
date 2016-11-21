import dbconn2
import MySQLdb
import os

db = 'dormdata_db'
Debug = False

def server(database):
	'''Returns a cursor to the database'''
	dsn = dbconn2.read_cnf('/home/cs304/.my.cnf')
	dsn['db'] = database
	conn = dbconn2.connect(dsn)
	conn.autocommit(True)
	return conn.cursor(MySQLdb.cursors.DictCursor)

def getDormNames(server):
	sql = "SELECT dorm_name from dorms"
	server.execute(sql)
	dorms = server.fetchall()
	return dorms

def getDormID(server, name):
	insert = '%' + name + '%'
	server.execute("SELECT did from dorms where dorm_name like %s", (insert,))
	row = server.fetchone()
	if row is None:
		return None
	return row['did']

def getDormInfo(server, did):
	server.execute("SELECT dorm_name, location from dorms where did = %s", (did,))
	row = server.fetchone()
	return (row['dorm_name'], row['location'])

def getReviews(server, did):
	server.execute("SELECT comment, username from review where did = %s", (did,))
	reviews = server.fetchall()
	return reviews

def averageRating(server, did):
	server.execute("SELECT rating from review where did = %s", (did,))
	ratings = server.fetchall()
	int_list = list(map(lambda x: int(x), ratings))
	return sum(int_list)/float(len(int_list))

def newReview(server, formData, dorm):
	dormID = getDormID(server, dorm)
	username = formData['username']
	comment = formData['comment']
	rating = formData['rating']
	sql = "INSERT into reviews(did, username, rating, comment) values (%s, %s, %s, %s)" % (dormID, username, comment, rating)

