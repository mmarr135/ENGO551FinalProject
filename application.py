#-------------------------------------------------------------------------------
# Name:         ENGO 551, Winter 2021, Final Project
# Student:      Alekhya Bhamidipati
#               Madison Marriott
#               Tanya Hegmann
# Created:      07-04-2021
#-------------------------------------------------------------------------------
#---------------SETUP---------------

import os
import csv #added on for csv read in
import json #built in json package to work with data
import requests

from flask import Flask, session, render_template, request, jsonify #Note added in request & render_template as they do in the lectures
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database from set URL
# DATABASE_URL = postgres://kevshpuonrwgfr:c8535cc284c9df961ecf0aa1657793e8de1632987c584b02216bbe401f4cb6f3@ec2-54-205-183-19.compute-1.amazonaws.com:5432/d67i21u3n79vhb
# Database Table referenced for login is = userlogin2
engine = create_engine(os.getenv("DATABASE_URL")) #Already preset as enviro variable
db = scoped_session(sessionmaker(bind=engine)) #main object to run SQL commands


def communitybound(name):
    x="https://data.calgary.ca/resource/surr-xmvs.geojson?name="
    query=x+name
    bound=requests.get(query)
    bounds=bound.json()
    return [bounds]

#---------------------------------------------------------------------
# --------------- HOMEPAGE ---------------

@app.route("/") #Home Route
def index():


    if 'user' in session: #check if currently signed in, ie, is a session in play
        username = session['user']
        return render_template("homesignedin.html", username = username) #Load HomePage where Session is Already Signed In

    return render_template("home.html") #Else Load Triaditional Home Page prompting to sign in



#---------------------------------------------------------------------
# --------------- lOG IN/SIGN IN PAGE ---------------

@app.route("/signin") #Sign in Route
def signin():

    return render_template("signin.html") #Load Sign In Page

#---------------------------------------------------------------------
# --------------- lOG IN/SIGN IN VERIFICATION PAGE ---------------

@app.route("/signincheck", methods=["POST"]) #Page to check if Log In Sucseeded or Failed
def signincheck():
    #check against database here

    #Assign temp variables to use as comparisons
    username = request.form.get("username_old")
    password = request.form.get("password_old")

    #Check against database

    checkuser = db.execute("SELECT * FROM userlogin2 WHERE (username = '{username}') AND (password = '{password}')".format(username = username, password = password)).fetchone()

    #if return false
    if checkuser is None:
        #ERROR SIGN IN TEMPLATE RUN
        return render_template("signinfail.html", username = username, password = password) #Load page for sign in Fail

    #else if return true...

    #start session
    session["user"] = username

    #run correct sign in
    return render_template("signinsuccess.html", username = username, password = password) #Load page for sign in Sucsess

#---------------------------------------------------------------------
# --------------- SIGN UP PAGE ---------------

@app.route("/signup") #Load Page to Sign Up At
def signup():

    return render_template("signup.html")

#---------------------------------------------------------------------
# --------------- SIGN UP VERIFICATION PAGE ---------------

@app.route("/signupcheck", methods=["POST"])
def signupcheck():
    #check against database here

    #Assign temp variables to use as comparisons
    username = request.form.get("username_new")
    password = request.form.get("password_new")

    #Check against database if Username already exists
    #Only need to check if username exists
    checkuser = db.execute("SELECT * FROM userlogin2 WHERE (username = '{username}')".format(username = username)).fetchone()

    #If username exists
        #error try again page

    #If Username does not already exist
    if checkuser is None:
        #Add Data to List
        db.execute("INSERT INTO userlogin2 (username, password) VALUES (:username, :password)",{"username":username, "password":password})
        db.commit()#commit changes

        #start session
        session["user"] = username

        return render_template("signupsuccess.html", username = username, password = password)

    #else if return true (aka username already exists)
    #run failed sign in
    return render_template("signupfail.html", username = username, password = password)

#---------------------------------------------------------------------
# --------------- LOGOUT PAGE ---------------

@app.route("/logout", methods=["POST"]) #Page where you can log out and end the session
def logout():

    username = session["user"] #retrieve username

    session.pop("user", None) #remove session, log out
    session.pop("book", None) #remove session data

    return render_template("userlogout.html", username = username)


#---------------------------------------------------------------------
# --------------- MAIN MAP PAGE ---------------

@app.route("/calgarycommunityhousingmap", methods=["POST"])
def calgarycommunityhousingmap():

    #retrieve session info
    username = session["user"]
    bound=None
    # retrieves list of communities for dropdown selection
    communities = db.execute("SELECT name FROM communities WHERE (class = 'Residential')").fetchall()
    communities=[i[0] for i in communities]

    # retrieves user selected community, gets bounds for map
    if request.method == 'POST':
        selectedcommunity = request.form.get("community")
    if selectedcommunity is not None:
        bound=communitybound(selectedcommunity)

    return render_template("calgarycommunityhousingmap.html", username = username, communities=communities, selectedcommunity=selectedcommunity, bound=bound)


#---------------------------------------------------------------------
# --------------- API ENDPOINT CODE ---------------

# Put API Endpoint page like books lab here
