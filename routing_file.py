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
	cursor = dorms.server()
	dorms = dorms.getDormNames()
	if request.method = "POST":
		dorm = request.form['dormname']
		if dorm != None:
			return redirect(url_for("view", dorm=dorm))
		else:
			flash("<p>Please choose a dorm.</p>")

	return render_template("homeDorm.html", dorms=dorms)

@app.route("/view/<dorm>", methods=["GET","POST"])
def view(dorm):
	cursor = dorms.server()
	dormID = dorms.getDormID(dorm)
	dormInfo = dorms.getDormInfo(cursor, dormID)
	location = dormInfo[1]
	reviews = dorms.getReviews(cursor, dormID)
	average_rating = dorms.averageRating(cursor, dormID)
	if request.method = "POST":
		dorms.newReview(cursor, request.form, dorm)
	return render_template("dormTemplate.html", dormName = dorm, dormLocation = location, dormReviews = reviews, dormRating = average_rating)

	if __name__ == '__main__':
	app.debug = True
	port = os.getuid()
	app.run('0.0.0.0',port)