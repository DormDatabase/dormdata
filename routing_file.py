import dbconn2
import dorms
from flask import Flask, render_template, flash, request, redirect, url_for
import MySQLdb
import os
app = Flask(__name__)
app.secret_key = "sdhgfbadpivcnxgmsre" #Secret key needed for message flashing

db = "dormdata_db"

@app.route("/", methods=["GET","POST"])
def index():
	cursor = dorms.server(db)
	dorm_name = dorms.getDormNames(cursor)
	print "Menu Populated"
	print request.method
	if request.method == "POST":
		print "going to get dorm name"
		dorm = request.form['dorm-select']
		print dorm
		if dorm != None:
			print "lol"
			return redirect(url_for("view", dorm=dorm))
		else:
			flash("<p>Please choose a dorm.</p>")

	return render_template("homeDorm.html", dorms=dorm_name)

@app.route("/view/<dorm>", methods=["GET","POST"])
def view(dorm):
	cursor = dorms.server(db)
	dormID = dorms.getDormID(cursor, dorm)
	dormInfo = dorms.getDormInfo(cursor, dormID)
	location = dormInfo[1]
	reviews = dorms.getReviews(cursor, dormID)
	print "here"
	average_rating = dorms.averageRating(cursor, dormID)
	if request.method == "POST":
		dorms.newReview(cursor, request.form, dorm)
		return redirect(url_for("view", dorm=dorm))
	return render_template("dormTemplate.html", dormName = dorm, dormLocation = location, dormReviews = reviews, dormRating = average_rating)

if __name__ == '__main__':
	app.debug = True
	port = os.getuid()
	app.run('0.0.0.0',port)