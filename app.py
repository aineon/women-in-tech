import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


# Renders home page
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


# Register user in the db
@app.route("/register")
def register():
    return render_template("register.html")


# Log existing user into site
@app.route("/login")
def login():
    return render_template("login.html")


# Displays all member profiles in the db
@app.route("/members")
def members():
    profiles = list(mongo.db.profiles.find())
    return render_template("members.html", profiles=profiles)


# Display full member profile
@app.route("/profile_detail/<profile_id>")
def profile_detail(profile_id):
    profile = mongo.db.profiles.find_one({"_id": ObjectId(profile_id)})
    return render_template("profile_detail.html",
                           profile=profile)


# Display members personal profile page
@app.route("/profile")
def my_profile():
    if session["user"]:
        my_profile = mongo.db.profiles.find_one(
                {"created_by": session["user"]})
        user = mongo.db.users.find_one({"username": session["user"]})
        connections = user["connections"]
        my_connections = []

        for con in connections:
            connection = mongo.db.profiles.find_one({"_id": ObjectId(con)})
            if connection is not None:
                my_connections.append(connection)

        return render_template("profile.html", profiles=my_profile,
                               my_connections=my_connections, user=user)


# Add another member as a connection
@app.route("/add_connection/<profile_id>", methods=["GET", "POST"])
def add_connection(profile_id):
    if request.method == "POST":
        user = mongo.db.users.find_one({"username": session["user"].lower()})
        connections = mongo.db.users.find_one(user)["connections"]
        # if member is already connected
        if ObjectId(profile_id) in connections:
            flash("You are already connected!")
            return redirect(url_for("members"))
        # otherwise adds member to users connections
        mongo.db.users.update_one(
             user, {"$push": {
                "connections": ObjectId(profile_id)}})
        flash("You are now connected!")
        return redirect(url_for("members"))


# Logs user out of their account
@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
