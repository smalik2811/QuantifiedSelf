# Importing all the required modules
import os
from flask import *
from flask_sqlalchemy import *
from sqlalchemy import and_

# Getting the path for the directory
current_dir = os.path.abspath(os.path.dirname(__file__))

# Creating the Flask app
app = Flask(__name__)

# Handling URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'

# Creating the database object of SQLAlchemy to handle all the database operations

db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

# Creating the Models for the Database Models

class Tracker(db.Model):
    __tablename__ = "tracker"
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    type = db.Column(db.String, nullable = False)
    settings = db.Column(db.String, nullable = False)
    last = db.Column(db.String, default = "Never")
    user = db.Column(db.String,db.ForeignKey("user.username"),nullable = False)

class Log(db.Model):
    __tablename__ = "log"
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    timestamp = db.Column(db.String)
    tracker = db.Column(db.String, db.ForeignKey("tracker.name"), nullable = False)
    value = db.Column(db.String, nullable = False)
    note = db.Column(db.String)
    user = db.Column(db.String,db.ForeignKey("user.username"),nullable = False)
    trackerid = db.Column(db.Integer, db.ForeignKey("tracker.id"),nullable = False)

class User(db.Model):
    __tablename__ = "user"
    name = db.Column(db.String, nullable = False)
    username = db.Column(db.String, primary_key = True, nullable = False)
    password = db.Column(db.String, nullable = False)

# Handling the Requests

@app.route("/",methods = ["GET","POST"])
def index():
    if request.method == "GET":
        return render_template("index.html",msg = "")
    elif request.method == "POST":
        user_input = request.form["user"]
        pass_input = request.form["pass"]
        user = User.query.filter_by(username = user_input).first()
        if not user:
            return render_template("index.html",msg = "No such username exist!")
        elif user_input == user.username and pass_input == user.password:
            return redirect("/home/{}".format(user.username))
        else:
            return render_template("index.html",msg = "Invalid username or password")

@app.route("/home/<username>")
def home(username):
    trackers = Tracker.query.filter_by(user = username).all()
    user = User.query.filter_by(username = username).first()
    return render_template("home.html",trackers = trackers,user = user)

@app.route("/<username>/tracker",methods = ["GET","POST"])
def addtracker(username):
    user = User.query.filter_by(username = username).first()
    if request.method == "GET":
        return render_template("addtracker.html",user = user, msg = "")
    else:
        tracker_name = request.form['name']
        tracker_desc = request.form['desc']
        tracker_type = request.form['tr_type']
        tracker_settings = request.form['settings']
        tracker = Tracker(name = tracker_name, description = tracker_desc,type = tracker_type, settings = tracker_settings,user = user.username)
        if not bool(Tracker.query.filter(and_(Tracker.name == tracker_name ,Tracker.user == user.username)).first()):
            db.session.add(tracker)
            db.session.commit()
            return redirect("/home/{}".format(user.username))
        else:
            return render_template("addtracker.html",msg = "Tracker already exists!")

@app.route("/<username>/tracker/<tracker_id>")
def show_tracker(username,tracker_id):
    user = User.query.filter_by(username = username).first()
    tracker = Tracker.query.filter_by(id = tracker_id).first()
    desc = tracker.description
    logs = Log.query.filter_by(trackerid = tracker_id)
    days = []
    values = []
    for log in logs:
        day = log.timestamp[:10] + " AT " + log.timestamp[11:]
        days.append(day)
        value = str(log.value)
        values.append(value)
    return render_template("summary.html",user = user, logs = logs,name = tracker.name,labels = days,datas = values,desc = desc)

@app.route("/<username>/<id>/log",methods = ["GET","POST"])
def addlog(username,id):
    tracker = Tracker.query.filter_by(id = id).first()
    user = User.query.filter_by(username = username).first()
    if request.method == "GET":
        data_type = tracker.type
        if data_type == "Numerical" or data_type == "Time Duration":
            value = "<input name = 'value' class='form-control' type='text'>"
            return render_template("addlog.html",user = user, tracker = tracker, input = value)
        elif data_type == "Multiple Choice" or data_type == "Boolean":
            if data_type == "Boolean":
                choices = ["True","False"]
            else:
                choices = tracker.settings.split(",")
            return render_template("addlog2.html",user = user, tracker = tracker, choices = choices)
    else:
        when = request.form['when']
        value = request.form['value']
        note = request.form['notes']
        log = Log(timestamp = when, value = value, note = note, tracker = tracker.name,user = user.username, trackerid = id)
        db.session.add(log)
        tracker = Tracker.query.filter_by(id = id).first()
        tracker.last = when[:10] + " AT " + when[11:]
        db.session.commit()
        return redirect("/home/{}".format(user.username))

@app.route("/signup",methods = ["GET","POST"])
def signup(msg = ""):
    if request.method == "GET":
        return render_template("signup.html")
    else:
        name = request.form['name']
        username = request.form['user']
        password = request.form['pass']
        con_passord = request.form['con_pass']
        if password == con_passord:
            if len(User.query.filter_by(username = username).all()) == 0:
                user = User(name = name, username = username, password = password)
                db.session.add(user)
                db.session.commit()
                return redirect("/")
            else:
                return redirect("signup.html","User already exist.")
        else:
            return render_template("signup.html","Confirmed password does not match.")

@app.route("/<username>/tracker/edit/<id>",methods = ["GET","POST"])
def editTracker(username,id):
    tracker = Tracker.query.filter_by(id = id).first()
    user = User.query.filter_by(username = username).first()
    if request.method == "GET":
        return render_template("edittracker.html",user = user, tracker = tracker)
    else:
        desc = request.form['desc']
        type = request.form['tr_type']
        settings = request.form['settings']
        tracker.description = desc
        tracker.type = type
        tracker.settings = settings
        db.session.commit()
        return redirect("/home/{}".format(user.username))

@app.route("/<username>/tracker/delete/<id>")
def deleteTracker(username,id):
    tracker = Tracker.query.filter_by(id = id).first()
    user = User.query.filter_by(username = username).first()
    db.session.delete(tracker)
    logs = Log.query.filter_by(trackerid = id).all()
    for log in logs:
        db.session.delete(log)
    db.session.commit()
    return redirect("/home/{}".format(user.username))

@app.route("/<username>/log/edit/<id>",methods = ["GET","POST"])
def editLog(username,id):
    log = Log.query.filter_by(id = id).first()
    user = User.query.filter_by(username = username).first()
    if request.method == "GET":
        return render_template("editlog.html",user = user, log = log)
    else:
        when = request.form['when']
        value = request.form['value']
        notes = request.form['notes']
        log.timestamp = when
        log.value = value
        log.notes = notes
        db.session.commit()
        return redirect("/home/{}".format(user.username))

@app.route("/<username>/log/delete/<id>")
def deleteLog(username,id):
    user = User.query.filter_by(username = username).first()
    log = Log.query.filter_by(id = id).first()
    db.session.delete(log)
    db.session.commit()
    return redirect("/home/{}".format(user.username))

# Running the Flask app
if __name__ == '__main__':
    app.debug = True
    app.run()