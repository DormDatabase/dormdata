import dbconn2
import MySQLdb
import os

db = 'dormdata_db'
Debug = False

def server(database):
	'''Returns a cursor to the database'''
	dsn = dbconn2.read_cnf('/students/dormdata/.my.cnf')
	dsn['db'] = database
	conn = dbconn2.connect(dsn)
	conn.autocommit(True)
	return conn.cursor(MySQLdb.cursors.DictCursor)

def getDormNames(server):
	server.execute("SELECT dorm_name from dorms")
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
	server.execute("SELECT comment, username from reviews where did = %s", (did,))
	reviews = server.fetchall()
	return reviews

def averageRating(server, did):
	server.execute("SELECT rating from reviews where did = %s", (did,))
	ratings = server.fetchall()
	ratingList = []
	for rate in ratings:
		ratingList.append(int(rate['rating']))
	if (len(ratingList) == 0):
		return 0
	return round(sum(ratingList)/float(len(ratingList)), 2)

def newReview(server, formData, dorm):
	dormID = getDormID(server, dorm)
	username = formData['username']
	comment = formData['comment']
	rating = formData['rating']
	server.execute("INSERT into reviews(did, username, rating, comment) values (%s, %s, %s, %s)", (dormID, username, rating, comment))
	
def newPic(server, filename, dorm):
	dormID = getDormID(server, dorm)
	server.execute("INSERT into pictures(did, address) values (%s, %s)", (dormID, filename))

def getPics(server, did):
	server.execute("SELECT address from pictures where did = %s", (did,))
	pics = server.fetchall()
	return pics
	

