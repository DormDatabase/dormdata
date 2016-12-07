import cgi_utils_sda
import dbconn2
import dorms
from flask import Flask, render_template, flash, request, redirect, url_for, session
from werkzeug import secure_filename
import MySQLdb
import os
app = Flask(__name__)
app.secret_key = "sdhgfbadpivcnxgmsre" #Secret key needed for message flashing and sessions

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
			
	if 'username' in session:
		username = session['username']
		login_status = "<p>username</p>"
	else:
		login_status = "<a href='/loginTemplate.html>Login</a>"
	return render_template("homeDorm.html", dorms=dorm_name, login_status=login_status)

@app.route("/view/<dorm>", methods=["GET","POST"])
def view(dorm):
	cursor = dorms.server(db)
	dormID = dorms.getDormID(cursor, dorm)
	dormInfo = dorms.getDormInfo(cursor, dormID)
	location = dormInfo[1]
	reviews = dorms.getReviews(cursor, dormID)
	average_rating = dorms.averageRating(cursor, dormID)
	dormPics = dorms.getPics(cursor, dormID)
	if 'username' in session:
		username = session['username']
		login_status = "<p>username</p>"
		if request.method == "POST":
			dorms.newReview(cursor, request.form, dorm, username)
			return redirect(url_for("view", dorm=dorm))
	else:
		login_status = "<a href='/login.html>Login</a>"
		flash("Must be logged in to review.")
	return render_template("dormTemplate.html", dormName = dorm, dormLocation = location, dormReviews = reviews, dormRating = average_rating, dormPics = dormPics, login_status=login_status)
	
@app.route("/upload/<dorm>", methods = ["GET", "POST"])
def upload(dorm):
	cursor = dorms.server(db)
	if 'username' in session:
		username = session['username']
		login_status = "<p>username</p>"
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
					dorms.newPic(cursor, filename, dorm, username)
					flash("File uploaded successfully")
				else:
					flash("File must be of type png, jpg, jpeg, or gif")
	else:
		login_status = "<a href='/login.html>Login</a>"
		flash("Must be logged in to upload pictures.")
	return render_template("uploadTemplate.html", dormName = dorm, login_status=login_status)
	
@app.route("/login", methods = ["GET", "POST"])
def login():
	cursor = dorms.server(db)
	if request.method = 'POST':
		user = request.['username']
		stored = dorm.getUser(cursor, user)
		if stored['username'] == user:
			if matchPassword(stored['password'],request.['password']):
				session['username'] = request.form['username']
				return redirect(url_for('index'))
			flash("Password was incorrect.")
		if dorms.isWellesley(user):
			dorms.newPerson(cursor, request.form)
			session['username'] = request.form['username']
			return redirect(url_for('index'))
		else:
			flash("Must be a Wellesley email.")
	return render_template("loginTemplate.hmtl")

@app.route("/logout")
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.debug = True
	port = os.getuid()
	app.run('0.0.0.0',port)