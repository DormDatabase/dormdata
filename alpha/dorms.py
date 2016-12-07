import dbconn2
import MySQLdb
import os
from werkzeug.security import generate_password_hash, \
	check_password_hash

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

def newReview(server, formData, dorm, username):
	dormID = getDormID(server, dorm)
	user = username
	comment = formData['comment']
	rating = formData['rating']
	server.execute("INSERT into reviews(did, username, rating, comment) values (%s, %s, %s, %s)", (dormID, user, rating, comment))
	
def newPic(server, filename, dorm, username):
	dormID = getDormID(server, dorm)
	server.execute("INSERT into pictures(did, username address) values (%s, %s)", (dormID, username, filename))

def getPics(server, did):
	server.execute("SELECT address from pictures where did = %s", (did,))
	pics = server.fetchall()
	return pics
	
def getUser(server, username):
	server.execute("SELECT * from people where username = %s", (username,))
	row = server.fetchone()
	if row == None:
		return None:
	return row

def hashPassword(password):
	return generate_password_hash(password)

def matchPassword(db_pass, password):
	return check_password_hash(db_pass, password)

def isWellesley(username):
	'''Idealy, this would be connected to Wellesley's CAS'''
	return "@wellesley" in username

def newPerson(server, formData):
	user = formData['username']
	hashed = generate_password_hash(formData['password'])
	server.execute("INSERT into person(username, password) values (%s, %s)", (user,hashed))
