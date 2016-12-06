import dbconn2
import dorms
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug import secure_filename
import MySQLdb
import os
app = Flask(__name__)
app.secret_key = "sdhgfbadpivcnxgmsre" #Secret key needed for message flashing

db = "dormdata_db"
UPLOAD_FOLDER = "images/"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER']	= UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET","POST"])
def index():
	cursor = dorms.server(db)
	dorm_name = dorms.getDormNames(cursor)
	if request.method == "POST":
		dorm = request.form['dorm-select']
		if dorm == "none":
			flash("Please choose a dorm")
		else:
			return redirect(url_for("view", dorm=dorm))
			

	return render_template("homeDorm.html", dorms=dorm_name)

@app.route("/view/<dorm>", methods=["GET","POST"])
def view(dorm):
	cursor = dorms.server(db)
	dormID = dorms.getDormID(cursor, dorm)
	dormInfo = dorms.getDormInfo(cursor, dormID)
	location = dormInfo[1]
	reviews = dorms.getReviews(cursor, dormID)
	average_rating = dorms.averageRating(cursor, dormID)
	dormPics = dorms.getPics(cursor, dormID)
	if request.method == "POST":
		dorms.newReview(cursor, request.form, dorm)
		return redirect(url_for("view", dorm=dorm))
	return render_template("dormTemplate.html", dormName = dorm, dormLocation = location, dormReviews = reviews, dormRating = average_rating, dormPics = dormPics)
	
@app.route("/upload/<dorm>", methods = ["GET", "POST"])
def upload(dorm):
	cursor = dorms.server(db)
	if request.method == 'POST':
		f = request.files['file']
		if f.filename == "":
			flash("No selected file. Try again.")
		else:
			if allowed_file(f.filename):
				filename = secure_filename(f.filename)
				f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				cmd = "chmod 777 images/" + filename
				os.system(cmd)
				dorms.newPic(cursor, filename, dorm)
				flash("File uploaded successfully")
			else:
				flash("File must be of type png, jpg, jpeg, or gif")
	return render_template("uploadTemplate.html", dormName = dorm)
	

		

if __name__ == '__main__':
	app.debug = True
	port = os.getuid()
	app.run('0.0.0.0',port)